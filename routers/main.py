from database.crud.chapter_crud import create_chapters
from database.crud.crud_enum import CrudEnum
from database.crud.manga_crud import get_manga_by_id, update_manga_meta
from commons.utils import construct_manga, construct_manga_base
from core.page import Page
from core.manga_site import MangaSite
from core.utils import get_manga_site_common
from pydantic.networks import HttpUrl
from database.crud import utils
import os
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi import Response, status

from sqlalchemy.orm import Session

from core.manga_catalog import MangaCatalog
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
    db_mangas = manga_crud.create_mangas(db, mangas, site)
    return [construct_manga_base(manga) for manga in db_mangas]



def read_img_to_b64(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        b = f.read()
        return base64.b64encode(b).decode("utf-8")


@router.get('/index/{site}/{manga_id}', response_model=Manga)
async def get_index(response: Response,
                    manga_id: int,
                    db: Session = Depends(get_db),
                    manga_site: MangaSite = Depends(get_manga_site_common)):
    db_manga = get_manga_by_id(db, manga_id)

    if db_manga is None:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"success": CrudEnum.Failed}
    
    thum_img = db_manga.thum_img
    
    if thum_img is not None and os.path.isfile(thum_img):
        os.remove(thum_img)
    
    manga = await manga_site.get_index_page(db_manga.url)
    create_chapters(db, manga)
    update_manga_meta(db, manga)

    for m_type, chapters in manga.chapters.items():
        chapters.reverse()

    return manga


@router.get('/chapter/{site}/{manga_id}')
async def get_chapter(response: Response, 
                      site: MangaSiteEnum,
                      manga_id: int,
                      page_url: HttpUrl,
                      manga_site: MangaSite = Depends(get_manga_site_common),
                      db: Session = Depends(get_db)):
    pages = chapter_crud.get_chapter_pages(db, page_url)
    if pages:
        pages = [Page.from_orm(page) for page in pages]
    else:
        db_manga = get_manga_by_id(db, manga_id)

        if db_manga is None:
            response.status_code = status.HTTP_406_NOT_ACCEPTABLE
            return {"success": CrudEnum.Failed}        

        pages = []

    async def img_gen():        
        if pages:            
            for page in pages:
                yield f'data: {json.dumps(page.dict())}\n\n'
        else:
            manga = construct_manga(db_manga)
            async for img_dict in manga_site.download_chapter(manga, page_url):
                img_dict['pic_path'] = img_dict['pic_path'].replace('static/', '')
                page = Page(**img_dict)                    
                pages.append(page)
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

@router.post('/create_site')
async def create_site(db: Session = Depends(get_db)):
    manga_site_crud.create_manga_site(db, MangaSiteEnum.CopyManga)
    return True


@router.get('/test')
async def test(db: Session = Depends(get_db)):
    db_pages = db.query(models.Page).all()
    for db_page in db_pages:
        db_page.pic_path = db_page.pic_path.replace('static/', '')
    # db_mangas = db.query(models.Manga).all()
    # for manga in db_mangas:        
    #     thum_img = manga.thum_img
    #     if thum_img is not None:
    #         manga.thum_img = thum_img.replace('static/', '')

    db.commit()
    

    return True
