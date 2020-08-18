from fastapi import Depends, APIRouter

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.config import Config

from database import schemas
from database.utils import get_db

from sqlalchemy.orm import Session
from auth.utils import create_access_token

router = APIRouter()

config = Config('.env')

COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = "localhost"
# COOKIE_DOMAIN = "127.0.0.1"


@router.get('/logout', tags=["security"])
async def logout():
    response = JSONResponse({"logout": True})
    response.delete_cookie(COOKIE_AUTHORIZATION_NAME, domain=COOKIE_DOMAIN)
    return response


@router.post("/login", response_model=schemas.Token, tags=["security"])
async def login(request: Request = None, db: Session = Depends(get_db)):
    token = await create_access_token(request, db)
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


