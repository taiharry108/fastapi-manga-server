from typing import Dict
from datetime import timedelta, datetime

from starlette.requests import Request
from starlette.config import Config
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import jwt

from google.oauth2 import id_token
from google.auth.transport import requests

from sqlalchemy.orm import Session

from database.crud import user_crud

config = Config('.env')
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
CLIENT_ID = config('GOOGLE_CLIENT_ID')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)


def extract_email_from_id_token(id_token_str: str) -> str:
    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str, requests.Request(), CLIENT_ID)
        check_issuer(idinfo=idinfo)
        return get_email(idinfo)

    except HTTPException as ex:
        raise HTTPException(
            status_code=ex.status_code, detail=ex.detail)


def create_access_token_from_data(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_header(request: Request):
    if not request.headers.get("X-Requested-With"):
        raise HTTPException(status_code=400, detail="Incorrect headers")


def check_issuer(idinfo: Dict[str, str]):
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise HTTPException(
            status_code=400, detail="Wrong issuer")


def get_email(idinfo: Dict[str, str]) -> str:
    if idinfo['email'] and idinfo['email_verified']:
        return idinfo["email"]
    else:
        raise HTTPException(
            status_code=400, detail="Unable to validate social login")


async def create_access_token(request: Request, db: Session) -> str:
    check_header(request)
    body_bytes = await request.body()
    auth_code = jsonable_encoder(body_bytes)

    email = extract_email_from_id_token(auth_code)
    user = user_crud.get_user_by_email(db, email, create_if_not_exist=True)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_from_data(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)
    return token
