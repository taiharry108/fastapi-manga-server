from core.manga import MangaSimple, Manga, MangaWithMeta
from database import models


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


def _construct_manga(manga: models.Manga, manga_type: MangaWithMeta, is_fav: bool):
    result = manga_type(name=manga.name, url=manga.url,
                        id=manga.id, site=manga.manga_site.name,
                        is_fav=is_fav)
    idx_retrieved = False
    for chapter in manga.chapters:
        result.add_chapter(chapter.type, chapter.title, chapter.page_url)
        idx_retrieved = True

    if idx_retrieved:
        result.retreived_idx_page()

    result.set_meta_data({
        'finished': manga.finished,
        'last_update': manga.last_update,
        'thum_img': manga.thum_img
    }, create_last_update=False)

    return result


def construct_simple_manga(manga: models.Manga, is_fav: bool) -> MangaSimple:
    return _construct_manga(manga, MangaSimple, is_fav)


def construct_manga(manga: models.Manga, is_fav: bool = None) -> Manga:
    return _construct_manga(manga, Manga, None)
