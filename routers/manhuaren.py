from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.manhuaren import ManHuaRen
from pydantic import BaseModel, HttpUrl

router = APIRouter()


class Manga(BaseModel):
    name: str
    url: HttpUrl


@router.get("/search/{search_keyword}", response_model=List[Manga])
async def search_manga(search_keyword: str):
    mhr = ManHuaRen()
    mangas = await mhr.search_manga(search_keyword)
    return [{"name": manga.name, "url": manga.url} for manga in mangas]


@router.get('/index/{manga_page}')
async def get_index(manga_page: str):
    mhr = ManHuaRen()
    url = f"{mhr.url}{manga_page.lstrip('/')}"
    manga = await mhr.get_index_page(url)
    return {"name": manga.name, "url": manga.url, "chapters": manga.chapters}

# @router.get('/chapter/{chapter_page}')
# async def get_index(chapter_page: str):
