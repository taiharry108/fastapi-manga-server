from pydantic import BaseModel, HttpUrl


class ChapterIn(BaseModel):
    page_url: HttpUrl


class Chapter(ChapterIn):
    title: str

    class Config:
        orm_mode = True
