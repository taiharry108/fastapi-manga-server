from enum import Enum
from database.crud import user_crud
from database import models
from sqlalchemy.orm import Session


def delete_all(db: Session) -> bool:
    db.query(models.Chapter).delete()

    for user in db.query(models.User).all():
        user.fav_mangas = []
        user.history = []
    db.commit()

    db.query(models.Manga).delete()
    db.query(models.User).delete()
    db.query(models.MangaSite).delete()
    db.query(models.History).delete()
    db.commit()
    return True
