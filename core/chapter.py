from typing import Optional
from pydantic import BaseModel, HttpUrl


class ChapterIn(BaseModel):
    id: Optional[int]
    page_url: HttpUrl


class Chapter(ChapterIn):
    title: str

    class Config:
        orm_mode = True
