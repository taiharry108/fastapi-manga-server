from typing import List
from database import models, schemas
from sqlalchemy.orm import Session


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



def add_fav_manga(db: Session, manga_id: int, user_id: int) -> bool:
    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)
    if db_manga and not db_manga in db_user.fav_mangas:
        db_user.fav_mangas.append(db_manga)
        db.commit()
        return True
    else:
        return False


def del_fav_manga(db: Session, manga_id: int, user_id: int) -> bool:
    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)
    if db_manga:
        db_user.fav_mangas.remove(db_manga)
        db.commit()
        return True
    else:
        return False


def get_fav_mangas(db: Session, user_id: int) -> List[models.Manga]:
    db_user = db.query(models.User).get(user_id)
    fav_mangas = db_user.fav_mangas
    return fav_mangas


def get_history_mangas(db: Session, user_id: int) -> List[models.Manga]:
    db_user = db.query(models.User).get(user_id)
    return db_user.history
    

def add_history_manga(db: Session, manga_id: int, user_id: int) -> bool:
    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)
    if db_manga and not db_manga in db_user.history:
        db_user.history.append(db_manga)
        db.commit()
        return True
    else:
        return False


def del_history_manga(db: Session, manga_id: int, user_id: int) -> bool:
    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)
    if db_manga:
        db_user.history.remove(db_manga)
        db.commit()
        return True
    else:
        return False
