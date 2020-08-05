from typing import List, Union
from .manga import Manga, MangaIndexTypeEnum
from .downloader import Downloader
from .manga_catalog import MangaCatalog
from .manga_site_enum import MangaSiteEnum

class MangaSite(object):
    def __init__(self, name, url):
        self._name = name
        self._url = url
        # self._manga_dict = {}
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

    name = property(get_name)
    url = property(get_url)
