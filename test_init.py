from tests.routers.test_database import override_get_db
from database import crud
from core.manga_site_enum import MangaSiteEnum
import os


db = next(override_get_db())

for site in list(MangaSiteEnum):
    site = crud.create_manga_site(db, site)
