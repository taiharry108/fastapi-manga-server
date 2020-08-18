from database import models, crud, utils
from .manga_site_enum import MangaSiteEnum
from .manga import Manga
from .utils import SingletonDecorator
from typing import Union


@SingletonDecorator
class MangaCatalog(object):
    def __init__(self):
        # self.__data = {site: {} for site in MangaSiteEnum}
        pass

    def construct_manga(self, manga: models.Manga) -> Manga:
        result = Manga(name=manga.name, url=manga.url)

        idx_retrieved = False

        for chapter in manga.chapters:
            m_type = chapter.type
            result.add_chapter(m_type, chapter.title, chapter.page_url)
            idx_retrieved = True
        
        if idx_retrieved:
            result.retreived_idx_page()

        result.set_meta_data({
            # 'last_update': manga.last_update,
            'finished': manga.finished,
        })

        return result

    def get_manga(self, site: MangaSiteEnum, manga_url: str, manga_name: str = None) -> Union[Manga, None]:
        """Get manga from manga url"""
        with utils.SQLAlchemyDBConnection() as conn:
            db = conn.session
            manga = crud.get_manga_by_url(db, manga_url)
            if manga is None:
                if manga_name is not None:

                    manga = crud.create_manga(
                        db, Manga(name=manga_name, url=manga_url), site)
                else:
                    return None
            return self.construct_manga(manga)

