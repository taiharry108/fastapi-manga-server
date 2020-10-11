from core.page import Page
from core.manga_site import MangaSite
from core.utils import get_manga_site_common
from pydantic.networks import HttpUrl
from database.crud import utils
from datetime import datetime, timedelta
import os
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from core.manga_catalog import MangaCatalog
from core.manga_site_factory import get_idx_page
from core.manga_site_enum import MangaSiteEnum
from core.manga import Manga, MangaBase
from database.crud import manga_crud, chapter_crud, manga_site_crud
from database.utils import get_db
from database import models

import base64
import json
router = APIRouter()
catalog = MangaCatalog()


@router.get("/search/{site}/{search_keyword}", response_model=List[MangaBase])
async def search_manga(site: MangaSiteEnum,
                       search_keyword: str,
                       db: Session = Depends(get_db),
                       manga_site: MangaSite = Depends(get_manga_site_common)):
    mangas = await manga_site.search_manga(search_keyword)
    manga_crud.create_mangas(db, mangas, site)
    return mangas


def read_img_to_b64(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        b = f.read()
        return base64.b64encode(b).decode("utf-8")


@router.get('/index/{site}/{manga_page}', response_model=Manga)
async def get_index(site: MangaSiteEnum,
                    manga_page: str,
                    db: Session = Depends(get_db),
                    manga_site: MangaSite = Depends(get_manga_site_common)):
    url = get_idx_page(site, manga_page)
    manga = catalog.get_manga(db, site, url)

    need_update = manga.last_update is None or manga.last_update + \
        timedelta(days=3) < datetime.now()

    # need_update = True

    if manga is None or not manga.idx_retrieved or need_update:
        if need_update and manga.thum_img is not None and os.path.isfile(manga.thum_img):
            os.remove(manga.thum_img)
        manga = await manga_site.get_index_page(url)
        chapter_crud.create_chapters(db, manga)
        manga_crud.update_manga_meta(db, manga)

    if manga.thum_img is not None:
        manga.thum_img = read_img_to_b64(manga.thum_img)

    for m_type, chapters in manga.chapters.items():
        chapters.reverse()

    return manga


@router.get('/chapter/{site}/{manga_page}')
async def get_chapter(site: MangaSiteEnum, manga_page: str,
                      page_url: HttpUrl,
                      manga_site: MangaSite = Depends(get_manga_site_common),
                      db: Session = Depends(get_db)):
    pages = chapter_crud.get_chapter_pages(db, page_url)
    if pages:
        pages = [Page.from_orm(page) for page in pages]
    else:
        url = get_idx_page(site, manga_page)

        manga = catalog.get_manga(db, site, url)
        if manga is None or not manga.idx_retrieved:
            manga = await manga_site.get_index_page(url)

        pages = []

    async def img_gen():        
        if pages:            
            for page in pages:
                yield f'data: {json.dumps(page.dict())}\n\n'
        else:
            async for img_dict in manga_site.download_chapter(manga, page_url):
                pages.append(Page(**img_dict))
                yield f'data: {json.dumps(img_dict)}\n\n'                
            chapter_crud.add_pages_to_chapter(db, page_url, pages)
        yield 'data: {}\n\n'

    return StreamingResponse(img_gen(), media_type="text/event-stream")


@router.delete('/all')
async def delete_all(db: Session = Depends(get_db)):
    success = utils.delete_all(db)
    for site in list(MangaSiteEnum):
        site = manga_site_crud.create_manga_site(db, site)
    return success


@router.delete('/all_pages')
async def delete_all_pages(db: Session = Depends(get_db)):
    db.query(models.Page).delete()
    db.commit()
    return True


@router.get('/test')
async def test(db: Session = Depends(get_db)):
    db_user = db.query(models.User).first()
    return True
