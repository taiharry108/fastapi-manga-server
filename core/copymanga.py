import binascii
import json
from typing import List, Union

from pydantic.networks import HttpUrl
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manga import Manga, MangaIndexTypeEnum
import re

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def decrypt(encrypted, passphrase, iv) -> str:
    encrypted = binascii.unhexlify(encrypted)
    encrypted = pad(encrypted, block_size=AES.block_size)
    aes = AES.new(passphrase.encode('utf-8'),
                  AES.MODE_CBC, iv.encode('utf-8'))

    decrypted = aes.decrypt(encrypted)
    
    end_idx = decrypted.rfind(b'}')
    end_idx = max(end_idx, decrypted.rfind(b']'))
    decrypted = decrypted[:end_idx + 1]
    try:
        decrypted = decrypted.decode('utf-8').strip()
    except:
        pass

    return decrypted


class CopyManga(MangaSite):
    def __init__(self):
        super(CopyManga, self).__init__(
            '拷貝漫畫', 'https://copymanga.net/'
        )
        self.site = MangaSiteEnum.CopyManga

    async def search_manga(self, keyword) -> List[Manga]:
        search_url = f'{self.url}api/kb/web/search/count?offset=0&platform=2&limit=12&q={keyword}'        
        result = await self.downloader.get_json(search_url)
        result = result['results']['comic']['list']
        result = [self.get_manga(self.site, item['name'], manga_url=f'{self.url}comic/{item["path_word"]}') for item in result]
        return result

    def get_meta_data(self, soup):
        span = soup.find('span', class_='comicParticulars-sigezi')
        last_update = span.findNext('span').text.strip()
        span2 = span.parent.findNext('li').select('span:nth-of-type(2)')
        finished = span.text == '已完結'
        thum_img = soup.find('img', class_='lazyload').get('data-src')

        return {'last_update': last_update, 'finished': finished, 'thum_img': thum_img}

    async def get_index_page(self, page: str) -> Manga:

        def get_type(idx_type) -> Union[None, MangaIndexTypeEnum]:
            type_ = None
            if idx_type == '話':
                type_ = MangaIndexTypeEnum.CHAPTER
            elif idx_type == '卷':
                type_ = MangaIndexTypeEnum.VOLUME
            elif idx_type == '番外篇':
                type_ = MangaIndexTypeEnum.MISC
            return type_
        
        
        soup = await self.downloader.get_soup(page)

        long_str = soup.find('div', class_='disposableData').get('disposable')
        passphrase = soup.find(
            'div', class_='disposablePass').get('disposable')
        iv = long_str[:16]
        encrypted = long_str[16:]
        data = json.loads(decrypt(encrypted, passphrase, iv))

        name = soup.find('div', class_='comicParticulars-title-right').find('h6').get('title')

        manga = self.get_manga(self.site, name, page)
        

        for key in data['default']['groups']:
            m_type = get_type(key)
            if m_type is None:
                continue
            for item in data['default']['groups'][key]:
                page_url = f'{page}/chapter/{item["uuid"]}'
                manga.add_chapter(
                    m_type, title=item['name'], page_url=page_url)
        
        meta_dict = self.get_meta_data(soup)
        thum_img_path = await self.downloader.get_img(meta_dict['thum_img'], download=True)
        meta_dict['thum_img'] = thum_img_path

        manga.set_meta_data(meta_dict)
        manga.retreived_idx_page()
        return manga

    async def get_page_urls(self, manga: Manga, page_url: HttpUrl) -> List[str]:
        soup = await self.downloader.get_soup(page_url)

        long_str = soup.find('div', class_='disposableData').get('disposable')
        passphrase = soup.find(
            'div', class_='disposablePass').get('disposable')
        iv = long_str[:16]
        encrypted = long_str[16:]
        data = json.loads(decrypt(encrypted, passphrase, iv))

        return [item['url'] for item in data]
