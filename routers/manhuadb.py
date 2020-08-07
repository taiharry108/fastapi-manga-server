from core.manga import MangaIndexTypeEnum
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.manhuadb import ManHuaDB 
from pydantic import BaseModel, HttpUrl
from core.manga_catalog import MangaCatalog
from core.manga_site_factory import MangaSiteEnum
router = APIRouter()
catalog = MangaCatalog()


class Manga(BaseModel):
    name: str
    url: HttpUrl


@router.get("/search/{search_keyword}", response_model=List[Manga])
async def search_manga(search_keyword: str):
    mhr = ManHuaDB()
    mangas = await mhr.search_manga(search_keyword)
    return [{"name": manga.name, "url": manga.url} for manga in mangas]


@router.get('/index/{manga_page}')
async def get_index(manga_page: str):
    mhr = ManHuaDB()
    url = f"{mhr.url}manhua/{manga_page.strip('/')}/"

    manga = catalog.get_manga(MangaSiteEnum.ManHuaDB, url)
    if manga is None or not manga.idx_retrieved:
        print(f"going to retrieve {url}")
        manga = await mhr.get_index_page(url)
    return {"name": manga.name, "url": manga.url, "chapters": manga.chapters}


@router.get('/chapter/{manga_page}')
async def get_index(manga_page: str, idx: int, m_type_int: int = 0):
    mhr = ManHuaDB()
    url = f"{mhr.url}manhua/{manga_page.strip('/')}/"

    manga = catalog.get_manga(MangaSiteEnum.ManHuaDB, url)
    if manga is None or not manga.idx_retrieved:
        print(f"going to retrieve {url}")
        manga = await mhr.get_index_page(url)

    if m_type_int == 0:
        m_type = MangaIndexTypeEnum.CHAPTER
    elif m_type_int == 1:
        m_type = MangaIndexTypeEnum.VOLUME
    else:
        m_type = MangaIndexTypeEnum.MISC    

    return StreamingResponse(mhr.download_chapter(manga, m_type, idx), media_type="text/event-stream")
