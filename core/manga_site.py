from typing import List, Union, AsyncIterable
from .manga import Manga
from .manga_index_type_enum import MangaIndexTypeEnum
from .downloader import Downloader
from .manga_catalog import MangaCatalog
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
        self.__catalog = MangaCatalog()

    def get_manga(self, site: MangaSiteEnum, manga_name: Union[str, None], manga_url: str) -> Manga:
        return self.__catalog.get_manga(site, manga_url, manga_name)

    def get_name(self) -> str:
        return self._name

    def get_url(self) -> str:
        return self._url

    async def search_manga(self, keyword: str) -> List[Manga]:
        """Search manga with keyword, returns a list of manga"""
        raise NotImplementedError

    async def get_index_page(self, page: str) -> Manga:
        raise NotImplementedError

    async def get_page_urls(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> List[str]:
        raise NotImplementedError

    async def download_chapter(self, manga: Manga, m_type: MangaIndexTypeEnum, idx: int) -> AsyncIterable[str]:
        img_urls = await self.get_page_urls(manga, m_type, idx)
        referer = manga.get_chapter(m_type, idx).page_url
        async for img_dict in self.downloader.get_images(img_urls, referer=referer):
            yield f'data: {json.dumps(img_dict)}\n\n'

        yield 'data: {}\n\n'

    name = property(get_name)
    url = property(get_url)
