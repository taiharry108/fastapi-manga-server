from commons.utils import construct_simple_manga
from fastapi import Response, status
from core.manga import MangaSimple
from typing import List
from database.crud import user_crud
from database.utils import get_current_active_user, get_db
from database import schemas

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/me", response_model=schemas.User, tags=["users"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.post("/add_fav/{manga_id}", tags=["users"], status_code=201)
async def add_fav(response: Response, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    success = user_crud.add_fav_manga(db, manga_id, user_id)    
    if not success:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"success": success}


@router.delete("/del_fav/{manga_id}", tags=["users"], status_code=202)
async def del_fav(response: Response, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    success = user_crud.del_fav_manga(db, manga_id, user_id)
    if not success:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"success": success}


@router.get("/favs", tags=["users"], response_model=List[MangaSimple])
async def get_favs(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    fav_mangas = user_crud.get_fav_mangas(db, user_id)
    return [construct_simple_manga(m, True) for m in fav_mangas]


@router.get("/history", tags=["users"], response_model=List[MangaSimple])
async def get_favs(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    history = user_crud.get_history_mangas(db, user_id)
    fav_mangas = user_crud.get_fav_mangas(db, user_id)
    fav_manga_ids = [manga.id for manga in fav_mangas]
    return [construct_simple_manga(m, m.id in fav_manga_ids) for m in history]


@router.post("/add_history/{manga_id}", tags=["users"], status_code=201)
async def add_history(response: Response, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    success = user_crud.add_history_manga(db, manga_id, user_id)
    if not success:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"success": success}


@router.delete("/del_history/{manga_id}", tags=["users"], status_code=202)
async def del_history(response: Response, current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db), manga_id: int = None):
    user_id = current_user.id
    success = user_crud.del_history_manga(db, manga_id, user_id)
    if not success:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
    return {"success": success}
