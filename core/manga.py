from .chapter import Chapter
from typing import Dict, List, Optional, Set
from .manga_index_type_enum import MangaIndexTypeEnum
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class MangaBase(BaseModel):
    id: int
    name: str
    url: HttpUrl

    class Config:
        orm_mode = True


class MangaWithMeta(MangaBase):
    last_update: Optional[datetime]
    finished: Optional[bool]
    thum_img: Optional[str]
    idx_retrieved: Optional[bool]

    def retreived_idx_page(self):
        self.idx_retrieved = True

    def set_meta_data(self, meta_data: dict, create_last_update=True):
        self.last_update = datetime.now() if create_last_update else meta_data.get('last_update')
        self.finished = meta_data.get('finished')
        self.thum_img = meta_data.get('thum_img')

    class Config:
        orm_mode = True


class Manga(MangaWithMeta):

    chapters: Dict[MangaIndexTypeEnum, List[Chapter]] = {
        m_site: [] for m_site in list(MangaIndexTypeEnum)}
    
    chapter_urls: Set[HttpUrl] = set()

    def add_chapter(self, m_type: MangaIndexTypeEnum, title: str, page_url: str):        
        if not page_url in self.chapter_urls:
            self.chapters[m_type].append(Chapter(title=title, page_url=page_url))
            self.chapter_urls.add(page_url)

    def get_chapter(self, m_type: MangaIndexTypeEnum, idx: int) -> Chapter:
        return self.chapters[m_type][idx]
