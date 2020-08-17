from typing import Optional
from datetime import timedelta, datetime
from pydantic import BaseModel
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)
from fastapi import HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder

from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse, HTMLResponse
from starlette.config import Config
import jwt
from jwt import PyJWTError
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

config = Config('.env')

COOKIE_AUTHORIZATION_NAME = "Authorization"
COOKIE_DOMAIN = "127.0.0.1"

CLIENT_SECRETS_JSON = config('GOOGLE_CLIENT_SECRETS_JSON')
CLIENT_ID = config('GOOGLE_CLIENT_ID')

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "Harry Chan",
        "email": "taiharry108@gmail.com",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        param = scheme = None

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")


def get_user_by_email(db, email: str):
    for username, value in db.items():
        if value.get("email") == email:
            user_dict = db[username]
            return User(**user_dict)


def authenticate_user_email(fake_db, email: str):
    user = get_user_by_email(fake_db, email)
    if not user:
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(fake_users_db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/swap_token", response_model=Token, tags=["security"])
async def swap_token(request: Request = None):
    if not request.headers.get("X-Requested-With"):
        raise HTTPException(status_code=400, detail="Incorrect headers")

    body_bytes = await request.body()
    auth_code = jsonable_encoder(body_bytes)

    try:
        idinfo = id_token.verify_oauth2_token(
            auth_code, requests.Request(), CLIENT_ID)
        print(idinfo)


        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        email = ""


        if idinfo['email'] and idinfo['email_verified']:
            email = idinfo.get('email')

        else:
            raise HTTPException(
                status_code=400, detail="Unable to validate social login")

    except:
        raise HTTPException(
            status_code=400, detail="Unable to validate social login")

    authenticated_user = authenticate_user_email(fake_users_db, email)

    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Incorrect email address")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)

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
async def get_open_api_endpoint(current_user: User = Depends(get_current_active_user)):
    response = "How cool is this?"
    return response


@router.get("/me", response_model=User, tags=["users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
