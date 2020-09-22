from database import models
from core.manga_site_enum import MangaSiteEnum
from sqlalchemy.orm import Session
from pydantic import HttpUrl
from core.manga import Manga
from typing import List
from .manga_site_crud import get_manga_site_id


def get_manga_by_url(db: Session, url: str) -> models.Manga:
    query_result = db.query(models.Manga).filter(models.Manga.url == url)
    return query_result.first()


def get_mangas_by_ids(db: Session, manga_ids: List[int]) -> List[models.Manga]:
    result = db.query(models.Manga).filter(
        models.Manga.id.in_(manga_ids)).all()
    return [next(s for s in result if s.id == id) for id in manga_ids]


def update_manga_meta(db: Session, manga: Manga) -> models.Manga:
    db_manga = get_manga_by_url(db, manga.url)
    db_manga.finished = manga.finished
    db_manga.last_update = manga.last_update
    db_manga.thum_img = manga.thum_img
    db.commit()
    return db_manga


def create_mangas(db: Session, mangas: List[Manga], site: MangaSiteEnum) -> bool:
    manga_site_id = get_manga_site_id(db, site)
    db_mangas = []

    urls = []

    for manga in mangas:
        urls.append(manga.url)

    db_mangas = db.query(models.Manga).filter(
        models.Manga.url.in_(urls)).all()

    url_set = set(m.url for m in db_mangas)

    for manga in mangas:
        if not manga.url in url_set:
            db_manga = models.Manga(
                name=manga.name, url=manga.url, manga_site_id=manga_site_id)
            db_mangas.append(db_manga)

    db.bulk_save_objects(db_mangas)
    db.commit()
    return True


def create_manga(db: Session, manga_name: str, manga_url: HttpUrl, site: MangaSiteEnum) -> models.Manga:
    manga_site_id = get_manga_site_id(db, site)
    db_manga = models.Manga(name=manga_name, url=manga_url,
                            manga_site_id=manga_site_id)
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga


def create_manga_with_manga_site_id(db: Session, manga_name: str, manga_url: HttpUrl, manga_site_id: int) -> models.Manga:
    db_manga = models.Manga(name=manga_name, url=manga_url,
                            manga_site_id=manga_site_id)
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga
