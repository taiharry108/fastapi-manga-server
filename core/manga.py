from enum import Enum
from .chapter import Chapter
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from MangaSite import MangaSite

class MangaIndexTypeEnum(Enum):
    CHAPTER = "Chapter"
    VOLUME = "Volume"
    MISC = "Misc"

class Manga(object):
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url
        self._chapters = {key: [] for key in list(MangaIndexTypeEnum)}
        self._last_update = None
        self._finished = None
        self._thum_img = None

    def add_chapter(self, m_type: MangaIndexTypeEnum, title: str, page_url: str):
        self._chapters[m_type].append(Chapter(title, page_url))

    def get_name(self) -> str:
        return self._name

    def get_url(self) -> str:
        return self._url

    def get_chapter(self, m_type: MangaIndexTypeEnum, idx: int) -> Chapter:
        return self._chapters[m_type][idx]

    def get_chapters(self) -> dict:
        return self._chapters

    def get_finished(self) -> bool:
        return self._finished

    def get_last_update(self) -> str:
        return self._last_update

    def get_thum_img(self) -> str:
        return self._thum_img

    def set_meta_data(self, meta_data: dict):
        self._last_update = meta_data.get('last_update')
        self._finished = meta_data.get('finished')
        self._thum_img = meta_data.get('thum_img')

    name = property(get_name)
    url = property(get_url)
    chapters = property(get_chapters)
    last_update = property(get_last_update)
    is_finished = property(get_finished)
    thum_img = property(get_thum_img)
