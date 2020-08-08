from core.manga_site_factory import get_idx_page, get_manga_site
from core.manga_site_enum import MangaSiteEnum
from core.manga import MangaIndexTypeEnum
from typing import List
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, HttpUrl
from core.manga_catalog import MangaCatalog
router = APIRouter()
catalog = MangaCatalog()


class Manga(BaseModel):
    name: str
    url: HttpUrl


@router.get("/search/{site}/{search_keyword}", response_model=List[Manga])
async def search_manga(site: MangaSiteEnum, search_keyword: str):
    manga_site = get_manga_site(site)
    mangas = await manga_site.search_manga(search_keyword)
    return [{"name": manga.name, "url": manga.url} for manga in mangas]


@router.get('/index/{site}/{manga_page}')
async def get_index(site: MangaSiteEnum, manga_page: str):
    manga_site = get_manga_site(site)
    url = get_idx_page(site, manga_page)

    manga = catalog.get_manga(MangaSiteEnum.ManHuaRen, url)
    if manga is None or not manga.idx_retrieved:
        print(f"going to retrieve {url}")
        manga = await manga_site.get_index_page(url)

    return {
        "name": manga.name,
        "url": manga.url,
        "chapters": manga.chapters,
        "lastUpdate": manga.last_update,
        "finished": manga.is_finished,
        "thumImg": manga.thum_img
    }


@router.get('/chapter/{site}/{manga_page}')
async def get_chapter(site: MangaSiteEnum, manga_page: str, idx: int, m_type_int: int = 0):
    manga_site = get_manga_site(site)
    url = get_idx_page(site, manga_page)

    manga = catalog.get_manga(MangaSiteEnum.ManHuaRen, url)
    if manga is None or not manga.idx_retrieved:
        print(f"going to retrieve {url}")
        manga = await manga_site.get_index_page(url)

    if m_type_int == 0:
        m_type = MangaIndexTypeEnum.CHAPTER
    elif m_type_int == 1:
        m_type = MangaIndexTypeEnum.VOLUME
    else:
        m_type = MangaIndexTypeEnum.MISC

    return StreamingResponse(manga_site.download_chapter(manga, m_type, idx), media_type="text/event-stream")
