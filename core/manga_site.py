from pathlib import Path
from typing import List, Union, AsyncIterable

from pydantic.networks import HttpUrl
from .manga import Manga
from .downloader import Downloader
from .manga_site_enum import MangaSiteEnum
import json


class MangaSite(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MangaSite, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name, url):
        self._name = name
        self._url = url
        self.downloader = Downloader()
        self.has_referer = True

    def get_manga(self, site: MangaSiteEnum, manga_name: Union[str, None], manga_url: str) -> Manga:
        return Manga(name=manga_name, url=manga_url, site=site)

    def get_name(self) -> str:
        return self._name

    def get_url(self) -> str:
        return self._url

    async def search_manga(self, keyword: str) -> List[Manga]:
        """Search manga with keyword, returns a list of manga"""
        raise NotImplementedError

    async def get_index_page(self, page: str) -> Manga:
        raise NotImplementedError

    async def get_page_urls(self, manga: Manga, page_url: HttpUrl) -> List[str]:
        raise NotImplementedError

    async def download_chapter(self, manga: Manga, page_url: HttpUrl) -> AsyncIterable[str]:
        img_urls = await self.get_page_urls(manga, page_url)
        referer = page_url if self.has_referer else None

        async for img_dict in self.downloader.get_images(img_urls, referer=referer):
            yield f'data: {json.dumps(img_dict)}\n\n'

        yield 'data: {}\n\n'
    
    async def download_chapter2(self, manga: Manga, page_url: HttpUrl) -> AsyncIterable[str]:
        img_urls = await self.get_page_urls(manga, page_url)
        referer = page_url if self.has_referer else None
        download_path = Path(self._name) / manga.name

        async for img_dict in self.downloader.get_images(img_urls, referer=referer, download_path=download_path):
            yield img_dict

    name = property(get_name)
    url = property(get_url)
