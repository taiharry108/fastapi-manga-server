import base64
from typing import List
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re
import json
from Crypto.Cipher import AES
from urllib import parse


class ManHuaBei(MangaSite):

    def decrypt(self, encrypted) -> str:
        encrypted = base64.b64decode(encrypted)
        passphrase = self.config['passphase']
        iv = self.config['iv']
        aes = AES.new(passphrase.encode('utf-8'),
                      AES.MODE_CBC, iv.encode('utf-8'))

        decrypted = aes.decrypt(encrypted)
        return decrypted.strip().decode('utf8')

    def decrypt_pages(self, s):
        decrypted = self.decrypt(s)
        idx = decrypted.find('"]')
        if idx != -1:
            decrypted = decrypted[:idx+2]
            pages = json.loads(decrypted)
        else:
            pages = []
        return pages

    def __init__(self):
        super(ManHuaBei, self).__init__(
            '漫畫唄', 'https://www.manhuabei.com/'
        )
        self.site = MangaSiteEnum.ManHuaBei
        self.img_domain = None
        with open('config/manhuabei_decrypt_config.json') as f:
            self.config = json.load(f)

    async def get_img_domain(self) -> str:
        """Get image domain"""
        if self.img_domain is not None:
            return self.img_domain
        url = f"{self.url}js/config.js"
        s = await self.downloader.get(url)
        match = re.search('resHost: (\[.*\]),\\r\\n', s)
        try:
            matched = match.group(1)
            d = json.loads(matched)
            self.img_domain = d[0]['domain'][0]
        except:
            self.img_domain = "https://mhimg.eshanyao.com"
        return self.img_domain

    async def search_manga(self, keyword) -> List[Manga]:

        def handle_li(li) -> Manga:
            a = li.find('a', class_='image-link')
            url = a.get('href')
            name = a.get('title').strip()
            if not url.startswith('http'):
                url = self.url + url.lstrip('/')
            manga = self.get_manga(self.site, name, url)
            return manga

        search_url = f'{self.url}search/?keywords={keyword}'
        soup = await self.downloader.get_soup(search_url)
        div = soup.find("div", {"id": "w0"})
        result = [handle_li(li)
                  for li in div.find_all("li", class_="list-comic")]
        return result

    def get_meta_data(self, soup):
        last_update = soup.find('span', class_='zj_list_head_dat')
        if last_update is not None:
            match = re.search(
                r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', last_update.text)
            if match:
                last_update = match.group(0)

        finished = soup.find('ul', class_='comic_deCon_liO').find(
            'a', {'href': '/list/wanjie/'}) is not None
        thum_img = soup.find(
            'div', class_='comic_i_img').find('img').get('src')

        return {'last_update': last_update, 'finished': finished, 'thum_img': thum_img}

    async def get_index_page(self, page: str) -> Manga:
        soup = await self.downloader.get_soup(page)

        name = soup.find('div', class_='comic_deCon').find('h1').text
        manga = self.get_manga(self.site, name, page)

        for m_type, ul_id in zip(MangaIndexTypeEnum, ["chapter-list-1", "chapter-list-4", "chapter-list-3"]):
            ul = soup.find('ul', {'id': ul_id})
            if ul is None:
                continue

            li_list = ul.find_all('li')
            for li in li_list:
                url = li.a.get('href').lstrip('/')
                if not url.startswith('http'):
                    url = 'https://www.manhuadui.com/' + url
                title = li.a.get('title')
                manga.add_chapter(m_type=m_type, title=title, page_url=url)

        meta_dict = self.get_meta_data(soup)
        thum_img_path = await self.downloader.get_img(meta_dict['thum_img'], download=True)
        meta_dict['thum_img'] = thum_img_path
        manga.set_meta_data(meta_dict)
        manga.retreived_idx_page()
        return manga

    def get_page_url(self, page_url: str, chap_path: str) -> str:
        encodeURI = parse.quote
        if re.search('^https?://(images.dmzj.com|imgsmall.dmzj.com)', page_url):
            return f'{self.img_domain}/showImage.php?url=' + encodeURI(page_url)
        if re.search('^[a-z]/', page_url):
            return f'{self.img_domain}/showImage.php?url=' + encodeURI("https://images.dmzj.com/" + page_url)
        if re.search("^(http:|https:|ftp:|^)//", page_url):
            return page_url
        filename = chap_path + '/' + page_url
        return self.img_domain + '/' + filename

    async def get_page_urls(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> List[str]:
        await self.get_img_domain()
        chapter = manga.get_chapter(m_type, idx)
        soup = await self.downloader.get_soup(chapter.page_url)

        pattern = re.compile(
            'chapterImages = "(.*)";var chapterPath = "(.*)";var chapterPrice')

        match = None
        for script in soup.find_all('script'):
            if len(script.contents) == 0:
                continue
            match = pattern.search(script.contents[0])
            if match:
                break
        if match:
            pages = self.decrypt_pages(match.group(1))
            chap_path = match.group(2).strip('/')

            pages = [self.get_page_url(page, chap_path) for page in pages]
            return pages

        return []
