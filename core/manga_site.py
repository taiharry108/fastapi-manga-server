from typing import List
from .manga import Manga, MangaIndexTypeEnum
from .downloader import Downloader

class MangaSite(object):
    def __init__(self, name, url):
        self._name = name
        self._url = url
        self._manga_dict = {}
        self.downloader = Downloader()

    def get_manga(self, manga_name, manga_url=None) -> Manga:
        if not manga_name in self._manga_dict.keys():
            assert manga_url is not None
            self._manga_dict[manga_name] = Manga(
                name=manga_name, url=manga_url)
        return self._manga_dict[manga_name]

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
