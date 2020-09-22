from tests.routers.utils import override_get_db
from database.crud import utils
from core.manga_site_enum import MangaSiteEnum
import os


db = next(override_get_db())

utils.delete_all(db)