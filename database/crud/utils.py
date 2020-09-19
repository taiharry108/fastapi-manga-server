from typing import Any, List
from database import models
from sqlalchemy.orm import Session


def delete_all(db: Session) -> bool:
    db.query(models.Chapter).delete()
    db.query(models.Manga).delete()
    db.query(models.User).delete()
    db.commit()
    return True

# def mass_create(db: Session, base: Any, objs: List[Any], unique_field: str):
#     l = []
#     for ob in objs:
#         l.append(getattr(ob, unique_field))
    
#     db.query(base).filter(models)


#     db_chaps = db.query(models.Chapter).filter(
#         models.Chapter.page_url.in_(urls)).all()

#     url_set = set(chap.page_url for chap in db_chaps)

#     for m_type, chapters in manga.chapters.items():
#         for chapter in chapters:
#             if not chapter.page_url in url_set:
#                 db_chaps.append(models.Chapter(**chapter.dict(),
#                                                manga_id=manga_id, type=m_type.value))

#     db.bulk_save_objects(db_chaps)
#     db.commit()
#     return True
