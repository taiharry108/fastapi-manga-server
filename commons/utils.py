from core.manga import Manga
from database import models


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


def construct_manga(manga: models.Manga) -> Manga:    
    result = Manga(name=manga.name, url=manga.url, id=manga.id, site=manga.manga_site.name)

    idx_retrieved = False        
    for chapter in manga.chapters:        
        m_type = chapter.type        
        result.add_chapter(m_type, chapter.title, chapter.page_url)
        idx_retrieved = True

    if idx_retrieved:
        result.retreived_idx_page()
    

    result.set_meta_data({
        'finished': manga.finished,
        'last_update': manga.last_update,
        'thum_img': manga.thum_img
    }, create_last_update=False)

    return result
