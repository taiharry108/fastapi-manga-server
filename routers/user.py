from commons.utils import construct_manga
from fastapi import Response, status
from core.manga import MangaWithMeta
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


@router.get("/favs", tags=["users"], response_model=List[MangaWithMeta])
async def get_favs(current_user: schemas.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    fav_mangas = user_crud.get_fav_mangas(db, user_id)
    return [construct_manga(m) for m in fav_mangas]
