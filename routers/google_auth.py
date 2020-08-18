from fastapi import Depends, APIRouter

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.config import Config

from database import schemas
from database.utils import get_current_active_user, get_db

from sqlalchemy.orm import Session
from auth import utils

router = APIRouter()

config = Config('.env')

COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = "localhost"


@router.get('/logout', tags=["security"])
async def logout():
    response = JSONResponse({"logout": True})
    response.delete_cookie(COOKIE_AUTHORIZATION_NAME, domain=COOKIE_DOMAIN)
    return response


@router.post("/login", response_model=schemas.Token, tags=["security"])
async def login(request: Request = None, db: Session = Depends(get_db)):
    token = await utils.create_access_token(request, db)
    response = JSONResponse({"access_token": token, "token_type": "bearer"})

    response.set_cookie(
        key=COOKIE_AUTHORIZATION_NAME,
        value=f"Bearer {token}",
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response


@router.get("/secure_endpoint", tags=["security"])
async def get_open_api_endpoint(current_user: schemas.User = Depends(get_current_active_user)):
    response = "How cool is this?"
    return response


@router.get("/me", response_model=schemas.User, tags=["users"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user
