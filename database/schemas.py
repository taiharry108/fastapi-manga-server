from core.manga_index_type_enum import MangaIndexTypeEnum
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, HttpUrl


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class MangaSite(BaseModel):
    name: str
    url: HttpUrl



