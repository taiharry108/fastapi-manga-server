from pydantic.main import BaseModel


class Page(BaseModel):
    pic_path: str
    idx: int
