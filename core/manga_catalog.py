from .manga_site_enum import MangaSiteEnum
from .manga import Manga
from .utils import SingletonDecorator
from typing import Union


@SingletonDecorator
class MangaCatalog(object):
    def __init__(self):        
        # will change to database
        self.__data = {site: {} for site in MangaSiteEnum}
    
    def _add_manga(self, site: MangaSiteEnum, manga: Manga):
        """Add manga to catalog"""        
        self.__data[site][manga.url] = manga
    
    def get_manga(self, site: MangaSiteEnum, manga_url: str, manga_name: str = None) -> Union[Manga, None]:
        """Get manga from manga url"""        
        if manga_url in self.__data[site]:
            return self.__data[site][manga_url]
        else:
            if manga_name is None:
                return None
            manga = Manga(manga_name, manga_url)
            self._add_manga(site, manga)
            return manga
    
    def get_num_manga(self, site: MangaSiteEnum):
        return len(self.__data[site])
    
    
    
