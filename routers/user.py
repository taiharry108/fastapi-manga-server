from core.manga import MangaBase
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


@router.post("/add_fav", tags=["users"])
async def add_fav(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    manga_id = 2
    return crud.add_fav_manga(db, manga_id, user_id)


@router.get("/favs", tags=["users"], response_model=List[MangaBase])
async def get_favs(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    fav_mangas = crud.get_fav_mangas(db, user_id)

    return fav_mangas
