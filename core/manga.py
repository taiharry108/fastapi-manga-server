from enum import Enum
from .chapter import Chapter
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from .manga_site import MangaSite

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
        self._idx_retrieved = False

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

    def get_finished(self) -> Union[bool, None]:
        return self._finished

    def get_last_update(self) -> Union[str, None]:
        return self._last_update

    def get_thum_img(self) -> Union[str, None]:
        return self._thum_img

    def get_idx_retrieved(self) -> bool:
        return self._idx_retrieved
    
    def retreived_idx_page(self):
        self._idx_retrieved = True

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
    idx_retrieved = property(get_idx_retrieved)
