from pydantic.main import BaseModel


class Page(BaseModel):
    pic_path: str
    idx: int
    total: int

    class Config:
        orm_mode = True
