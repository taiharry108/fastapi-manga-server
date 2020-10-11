from database.crud.crud_enum import CrudEnum
from database.crud import manga_crud
from datetime import datetime
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
    History = models.History
    history_mangas = db.query(History).order_by(
        History.last_added.desc()).filter(History.user_id == user_id)

    history_manga_ids = [
        history.manga_id for history in history_mangas]

    return manga_crud.get_mangas_by_ids(db, history_manga_ids)


def manga_in_user_history(db: Session, manga_id: int, user_id: int) -> models.History:
    History = models.History
    return db.query(History).filter(History.manga_id == manga_id, History.user_id == user_id).first()


def add_history_manga(db: Session, manga_id: int, user_id: int) -> CrudEnum:
    History = models.History

    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)

    if db_manga is None or db_user is None:
        status = CrudEnum.Failed
    else:
        db_hist = db.query(History).filter(History.manga_id ==
                                           manga_id, History.user_id == user_id).first()
        if db_hist is None:
            db_hist = models.History(
                last_added=datetime.now(), user=db_user, manga=db_manga)
            status = CrudEnum.Created
        else:
            db_hist.last_added = datetime.now()
            status = CrudEnum.Updated

    db.commit()
    return status


def del_history_manga(db: Session, manga_id: int, user_id: int) -> CrudEnum:
    History = models.History

    db_manga = db.query(models.Manga).get(manga_id)
    db_user = db.query(models.User).get(user_id)

    if db_manga is None or db_user is None:
        status = CrudEnum.Failed
    else:
        db_hist = db.query(History).filter(History.manga_id ==
                                           manga_id, History.user_id == user_id).first()
        if db_hist is None:
            status = CrudEnum.Failed
        else:
            db.delete(db_hist)
            status = CrudEnum.Deleted
            db.commit()
    return status
