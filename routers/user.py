from core.manga import MangaBase, MangaWithMeta
from typing import List
from database import crud
from database.utils import get_current_active_user, get_db
from database import schemas

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/me", response_model=schemas.User, tags=["users"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.post("/add_fav/{manga_id}", tags=["users"])
async def add_fav(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    return {"success": crud.add_fav_manga(db, manga_id, user_id)}


@router.delete("/del_fav/{manga_id}", tags=["users"])
async def del_fav(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    return {"success": crud.del_fav_manga(db, manga_id, user_id)}


@router.get("/favs", tags=["users"], response_model=List[MangaWithMeta])
async def get_favs(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    fav_mangas = crud.get_fav_mangas(db, user_id)
    return fav_mangas
