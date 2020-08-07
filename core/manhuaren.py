from typing import List, AsyncIterable, Dict, Any
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re
import string
import json

digs = string.digits + string.ascii_letters


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


def decode(p, a: int, c: int, k, d):
    def e(c: int) -> str:
        first = "" if c < a else e(int(c/a))
        c = c % a
        if c > 35:
            second = chr(c + 29)
        else:
            second = int2base(c, 36)
        return first + second
    while c != 0:
        c -= 1
        d[e(c)] = k[c] if k[c] != "" else e(c)
    k = [lambda x: d[x]]
    def e2(): return '\\w+'
    c = 1
    while c != 0:
        c -= 1
        p = re.sub(f'\\b{e2()}\\b', lambda x: k[c](x.group()), p)
    return p


class ManHuaRen(MangaSite):
    def __init__(self):
        super(ManHuaRen, self).__init__(
            '漫畫人', 'https://www.manhuaren.com/'
        )
        self.site = MangaSiteEnum.ManHuaRen

    async def search_manga(self, keyword) -> List[Manga]:

        def handle_div(div) -> Manga:
            name = div.find('p', class_='book-list-info-title').text
            url = div.find('a').get('href')
            if not url.startswith('http'):
                url = self.url + url.lstrip('/')
            manga = self.get_manga(self.site, name, url)
            return manga

        search_url = f'{self.url}search?title={keyword}&language=1'
        soup = await self.downloader.get_soup(search_url)
        result = [handle_div(d) for d in soup.find('ul', class_='book-list').find_all(
            'div', class_='book-list-info')]
        return result

    async def get_index_page(self, page: str) -> Manga:

        def get_type(idx_type):
            if idx_type == '连载':
                type_ = MangaIndexTypeEnum.CHAPTER
            elif idx_type == '单行本':
                type_ = MangaIndexTypeEnum.VOLUME
            else:
                type_ = MangaIndexTypeEnum.MISC
            return type_

        manga = self.get_manga(self.site, None, page)

        if manga is not None:
            return manga

        soup = await self.downloader.get_soup(page)

        name = soup.find('p', class_='detail-main-info-title').text

        div = soup.find('div', class_='detail-selector')

        id_dict = {}

        for a in div.find_all('a', 'detail-selector-item'):
            onclick = a.get('onclick')
            if 'titleSelect' in onclick:
                id_dict[a.text] = onclick.split("'")[3]

        manga = self.get_manga(self.site, name, page)

        for idx_type, id_v in id_dict.items():
            ul = soup.find('ul', {'id': id_v})
            m_type = get_type(idx_type)
            for a in ul.find_all('a'):
                url = a.get('href')
                if not url.startswith('http'):
                    url = self.url + url.lstrip('/')
                title = a.text
                manga.add_chapter(m_type=m_type, title=title, page_url=url)

        manga.retreived_idx_page()
        # manga.set_meta_data(self.get_meta_data(soup))
        return manga

    async def get_page_urls(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> List[str]:
        chapter = manga.get_chapter(m_type, idx)
        soup = await self.downloader.get_soup(chapter.page_url)

        match = None
        for script in soup.find_all('script'):
            if len(script.contents) == 0:
                continue
            if script.contents[0].startswith('eval'):
                match = re.search('return p;}(.*\))\)', script.contents[0])
                break
        if match:
            tuple_str = match.group(1)
            p, a, c, k, e, d = eval(tuple_str)
            p = decode(p, a, c, k, d)

            match2 = re.search(r'var newImgs=(.*);', p)
            if match2:
                pages = eval(match2.group(1))
                return pages
        return []

    async def download_chapter(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> AsyncIterable[str]:
        img_urls = await self.get_page_urls(manga, m_type, idx)
        async for img_dict in self.downloader.get_images(img_urls):
            yield f'data: {json.dumps(img_dict)}\n\n'
        
        yield 'data: {}\n\n'
