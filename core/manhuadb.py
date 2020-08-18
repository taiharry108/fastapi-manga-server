from typing import List
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re
import json
import base64


class ManHuaDB(MangaSite):
    def __init__(self):
        super(ManHuaDB, self).__init__(
            '漫畫DB', 'https://www.manhuadb.com/'
        )
        self.site = MangaSiteEnum.ManHuaDB

    async def search_manga(self, keyword) -> List[Manga]:

        def handle_div(div) -> Manga:
            name = div.find('a').get('title')
            url = div.find('a').get('href')
            if not url.startswith('http'):
                url = self.url + url.strip('/') + "/"
            manga = self.get_manga(self.site, name, url)
            return manga

        search_url = f'{self.url}search?q={keyword}'
        soup = await self.downloader.get_soup(search_url)
        result = [handle_div(d) for d in soup.find_all(
            'div', class_='comicbook-index')]
        return result
    
    def get_meta_data(self, soup):
        table = soup.find(
            'table', class_='comic-meta-data-table')
        last_update = ""
        finished = table.find('a', class_='comic-pub-state').text != '连载中'
        thum_img = table.find(
            'td', class_='comic-cover').find('img').get('src')

        if not thum_img.startswith('http'):
            thum_img = self.url + thum_img.lstrip('/')

        return {'last_update': last_update, 'finished': finished, 'thum_img': thum_img}

    async def get_index_page(self, page: str) -> Manga:

        type_names = {'连载', '单行本', '番外篇'}

        def get_type(idx_type):
            if idx_type == '连载':
                type_ = MangaIndexTypeEnum.CHAPTER
            elif idx_type == '单行本':
                type_ = MangaIndexTypeEnum.VOLUME
            else:
                type_ = MangaIndexTypeEnum.MISC
            return type_

        soup = await self.downloader.get_soup(page)

        name = soup.find('h1', class_='comic-title').text
        manga = self.get_manga(self.site, name, page)

        ul = soup.find('ul', {'id': 'myTab'})
        a_list = ul.find_all('a', class_='nav-link')
        id_dict = {a.find('span').text: a.get('aria-controls')
                   for a in a_list if a.find('span').text in type_names}

        div = soup.find('div', {'id': 'comic-book-list'})

        for idx_type, id_v in id_dict.items():
            tab = div.find('div', {'id': id_v})
            m_type = get_type(idx_type)
            for li in tab.find_all('li'):
                a = li.find('a')
                title = a.get('title')
                url = a.get('href')
                if not url.startswith('http'):
                    url = self.url + url.lstrip('/')
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

        match = None

        pattern = re.compile(r"var img_data = '(.*)'")
        for script in soup.find_all('script'):
            if len(script.contents) == 0:
                continue
            match = pattern.search(script.contents[0])
            if match:
                break
        
        if match is None:
            return []

        decoded = base64.b64decode(match.group(1))
        decoded_list = json.loads(decoded)

        vgr_data = soup.find('div', 'vg-r-data')
        host = vgr_data.get('data-host')
        img_pre = vgr_data.get('data-img_pre')
        pages = [f'{host}{img_pre}{d["img_webp"]}' for d in decoded_list]
        
        return pages
