from typing import List
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re
import string
import lzstring
import json
digs = string.digits + string.ascii_letters


def decompress(s):
    x = lzstring.LZString()
    return x.decompressFromBase64(s)

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


class ManHuaGui(MangaSite):
    def __init__(self):
        super(ManHuaGui, self).__init__(
            '漫畫櫃', 'https://www.manhuagui.com/'
        )
        self.site = MangaSiteEnum.ManHuaRen

    async def search_manga(self, keyword) -> List[Manga]:

        def handle_div(div) -> Manga:
            dt = div.find('dt')
            name = dt.find('a').get('title')
            url = dt.find('a').get('href')
            if not url.startswith('http'):
                url = self.url + url.lstrip('/')
            manga = self.get_manga(self.site, name, url)
            return manga

        search_url = f'{self.url}s/{keyword}.html'
        soup = await self.downloader.get_soup(search_url)
        result_div = soup.find("div", {"class": "book-result"})
        result = [handle_div(div) for div in result_div.find_all(
            "div", {"class": "book-detail"})]
        return result

    def get_meta_data(self, soup):
        spans = soup.find('li', class_='status').find_all('span', class_='red')
        last_update = spans[-1].text.strip()
        finished = spans[0].text != '连载中'
        thum_img = soup.find('div', class_='book-cover').find('img').get('src')

        if not thum_img.startswith('http'):
            thum_img = self.url + thum_img.lstrip('/')

        return {'last_update': last_update, 'finished': finished, 'thum_img': thum_img}

    async def get_index_page(self, page: str) -> Manga:

        def get_type(idx_type):
            if idx_type == '单话':
                type_ = MangaIndexTypeEnum.CHAPTER
            elif idx_type == '单行本':
                type_ = MangaIndexTypeEnum.VOLUME
            else:
                type_ = MangaIndexTypeEnum.MISC
            return type_

        soup = await self.downloader.get_soup(page)

        name = soup.find('div', class_='book-title').find('h1').text
        manga = self.get_manga(self.site, name, page)

        div = soup.find('div', class_='chapter')
        idx_types = [h4.find('span').text for h4 in div.find_all('h4')]
        divs = div.find_all('div', class_='chapter-list')

        for idx_type, div in zip(idx_types, divs):
            m_type = get_type(idx_type)
            for ul in div.find_all('ul'):
                for a in reversed(ul.find_all('a')):
                    title = a.get('title')
                    url = a.get('href')
                    if not url.startswith('http'):
                        url = f"{self.url}{url.lstrip('/')}"
                    manga.add_chapter(m_type=m_type, title=title, page_url=url)
        
        meta_dict = self.get_meta_data(soup)
        thum_img_path = await self.downloader.get_img(meta_dict['thum_img'], download=True)
        meta_dict['thum_img'] = thum_img_path
        manga.set_meta_data(meta_dict)
        manga.retreived_idx_page()
        return manga

    async def get_page_urls(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> List[str]:
        chapter = manga.get_chapter(m_type, idx)        
        soup = await self.downloader.get_soup(chapter.page_url)

        pattern = re.compile('window.*return p;}(.*\))\)')
        
        match = None
        for script in soup.find_all('script'):
            if len(script.contents) == 0:
                continue
            match = pattern.search(script.contents[0])
            if match:
                break
        
        if match:
            p, a, c, k, e, d = eval(match.group(1).replace(
                r"['\x73\x70\x6c\x69\x63']('\x7c')", ""))
            p = decode(p, a, c, decompress(k).split('|'), d)

            match = re.search('SMH.imgData\((.*)\).preInit', p)
            manga_data = json.loads(match.group(1))
            path = manga_data['path']
            e = manga_data["sl"]["e"]
            m = manga_data["sl"]["m"]
            pages = []
            for file in manga_data['files']:
                page_url = f"https://i.hamreus.com{path}{file}?e={e}&amp;m={m}"
                pages.append(page_url)
            return pages

        return []

    
