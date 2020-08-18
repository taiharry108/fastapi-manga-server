from fastapi import HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
from jwt import PyJWTError
from starlette.config import Config
from .oauth2_password_bearer_cookie import OAuth2PasswordBearerCookie

from database import schemas
from database.database import SessionLocal
from database.crud import get_user_by_email

import jwt
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")
config = Config('.env')
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


class SQLAlchemyDBConnection(object):
    """SQLAlchemy database connection"""

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()



def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):    
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
