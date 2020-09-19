from database import models, crud, utils
from database.crud import manga_crud
from .manga_site_enum import MangaSiteEnum
from .manga import Manga
from commons.utils import SingletonDecorator, construct_manga
from typing import Union


@SingletonDecorator
class MangaCatalog(object):
    def __init__(self):
        # self.__data = {site: {} for site in MangaSiteEnum}
        pass

    def get_manga(self, site: MangaSiteEnum, manga_url: str, manga_name: str = None) -> Union[Manga, None]:
        """Get manga from manga url"""
        with utils.SQLAlchemyDBConnection() as conn:
            db = conn.session
            manga = manga_crud.get_manga_by_url(db, manga_url)
            if manga is None:
                if manga_name is not None:
                    manga = manga_crud.crud.create_manga(
                        db, manga_name, manga_url, site)
                else:
                    return None

            return construct_manga(manga)
