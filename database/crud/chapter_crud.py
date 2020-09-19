from database import models
from core.manga_index_type_enum import MangaIndexTypeEnum
from sqlalchemy.orm import Session
from core.chapter import Chapter
from core.manga import Manga
from .manga_crud import get_manga_by_url

def create_chapter(db: Session, chapter: Chapter, manga_id: int, m_type: MangaIndexTypeEnum):
    db_chap = models.Chapter(
        **chapter.dict(), manga_id=manga_id, type=m_type.value)
    db.add(db_chap)
    db.commit()
    db.refresh(db_chap)
    return db_chap


def create_chapters(db: Session, manga: Manga) -> bool:
    db_manga = get_manga_by_url(db, manga.url)
    if db_manga is None:
        db_manga = create_manga(db, manga.name, manga.url, manga.site)

    manga_id = manga.id = db_manga.id

    db_chaps = []

    urls = []

    for m_type, chapters in manga.chapters.items():
        for chapter in chapters:
            urls.append(chapter.page_url)

    db_chaps = db.query(models.Chapter).filter(
        models.Chapter.page_url.in_(urls)).all()

    url_set = set(chap.page_url for chap in db_chaps)

    for m_type, chapters in manga.chapters.items():
        for chapter in chapters:
            if not chapter.page_url in url_set:
                db_chaps.append(models.Chapter(**chapter.dict(),
                                               manga_id=manga_id, type=m_type.value))

    db.bulk_save_objects(db_chaps)
    db.commit()
    return True


def get_chapter_by_url(db: Session, url: str) -> models.Chapter:
    query_result = db.query(models.Chapter).filter(
        models.Chapter.page_url == url)
    return query_result.first()
