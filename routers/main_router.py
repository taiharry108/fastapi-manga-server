from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from core.manga_catalog import MangaCatalog
from core.manga_site_factory import get_idx_page, get_manga_site
from core.manga_site_enum import MangaSiteEnum
from core.manga_index_type_enum import MangaIndexTypeEnum
from core.manga import Manga, MangaBase
from database import crud
from database.utils import get_db
router = APIRouter()
catalog = MangaCatalog()


@router.get("/search/{site}/{search_keyword}", response_model=List[MangaBase])
async def search_manga(site: MangaSiteEnum, search_keyword: str):
    manga_site = get_manga_site(site)
    mangas = await manga_site.search_manga(search_keyword)
    return mangas


@router.get('/index/{site}/{manga_page}', response_model=Manga)
async def get_index(site: MangaSiteEnum, manga_page: str, db: Session = Depends(get_db)):
    manga_site = get_manga_site(site)
    url = get_idx_page(site, manga_page)
    manga = catalog.get_manga(site, url)
    if manga is None or not manga.idx_retrieved or manga.last_update + timedelta(days=3) < datetime.now():
        manga = await manga_site.get_index_page(url)
        crud.create_chapters(db, manga)
        crud.update_manga_meta(db, manga)

    return manga


@router.get('/chapter/{site}/{manga_page}')
async def get_chapter(site: MangaSiteEnum, manga_page: str, idx: int, m_type_int: int = 0):
    manga_site = get_manga_site(site)
    url = get_idx_page(site, manga_page)

    manga = catalog.get_manga(site, url)
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


# @router.get('/test')
# async def test(db: Session = Depends(get_db)):
#     site = crud.create_manga_site(db, MangaSiteEnum.ManHuaGui)
#     return site
