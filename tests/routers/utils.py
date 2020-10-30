from pathlib import Path
from core.manga_site_factory import get_manga_site
from core.manga_site import MangaSite
from core.manga_site_enum import MangaSiteEnum
from database.crud.user_crud import get_user_by_email
from database.schemas import User
from sqlalchemy.orm import Session
from database.utils import get_db
from fastapi.param_functions import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from database.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


async def override_get_manga_site_common(site: MangaSiteEnum) -> MangaSite:
    manga_site = get_manga_site(site)
    manga_site.downloader.download_dir = Path('./static/test_images')
    return manga_site


def override_oauth2_scheme(request: Request):
    return True


async def override_get_current_user(token: str = Depends(override_oauth2_scheme), db: Session = Depends(get_db)):
    return get_user_by_email(db, "test@gmail.com")


async def override_get_current_active_user(current_user: User = Depends(override_get_current_user)):
    return current_user
