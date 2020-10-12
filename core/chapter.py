from pydantic import BaseModel, HttpUrl

class Chapter(BaseModel):
    title: str
    page_url: HttpUrl

    class Config:
        orm_mode = True