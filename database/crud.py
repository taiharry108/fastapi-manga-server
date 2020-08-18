from typing import List
from core.manga_index_type_enum import MangaIndexTypeEnum
from core.manga_site_enum import MangaSiteEnum
from sqlalchemy.orm import Session
from database import models, schemas
from core.manga import Manga
from core.chapter import Chapter


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str, create_if_not_exist: bool = False) -> models.User:
    result = db.query(models.User).filter(models.User.email == email).first()
    if result is None and create_if_not_exist:
        result = create_user(db, schemas.UserCreate(email=email))
    return result


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_manga_by_url(db: Session, url: str) -> models.Manga:
    query_result = db.query(models.Manga).filter(models.Manga.url == url)
    return query_result.first()


def update_manga_meta(db: Session, manga: Manga) -> models.Manga:
    db_manga = get_manga_by_url(db, manga.url)
    db_manga.finished = manga.finished
    db_manga.last_update = manga.last_update
    db.commit()
    return db_manga


def create_manga(db: Session, manga: Manga, site: MangaSiteEnum) -> models.Manga:
    manga_site_id = get_manga_site_id(db, site)
    db_manga = models.Manga(name=manga.name, url=manga.url,
                            manga_site_id=manga_site_id)
    db.add(db_manga)
    db.commit()
    db.refresh(db_manga)
    return db_manga


def create_manga_site(db: Session, site: MangaSiteEnum):
    from core import manga_site_factory
    url = manga_site_factory.get_manga_site(site).url
    db_manga_site = models.MangaSite(
        name=site.value,
        url=url)
    db.add(db_manga_site)
    db.commit()
    db.refresh(db_manga_site)
    return db_manga_site


def delete_manga_sites(db: Session):
    return db.query(models.MangaSite).delete()


def get_manga_site_id(db: Session, site: MangaSiteEnum) -> int:
    return db.query(models.MangaSite).filter(models.MangaSite.name == site.value).first().id


def create_chapter(db: Session, chapter: Chapter, manga_id: int, m_type: MangaIndexTypeEnum):
    db_chap = models.Chapter(
        **chapter.dict(), manga_id=manga_id, type=m_type.value)
    db.add(db_chap)
    db.commit()
    db.refresh(db_chap)
    return db_chap


def create_chapters(db: Session, manga: Manga) -> bool:
    manga_id = get_manga_by_url(db, manga.url).id
    db_chaps = []
    for m_type, chapters in manga.chapters.items():
        for chapter in chapters:
            db_chaps.append(models.Chapter(**chapter.dict(), manga_id=manga_id, type=m_type.value))
    db.bulk_save_objects(db_chaps)
    db.commit()
    return True
