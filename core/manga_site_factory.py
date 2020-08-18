
from .manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum



def get_manga_site(manga_site_enum: MangaSiteEnum) -> MangaSite:
    from .manhuaren import ManHuaRen
    if manga_site_enum == MangaSiteEnum.ManHuaRen:
        return ManHuaRen()
    elif manga_site_enum == MangaSiteEnum.ManHuaDB:
        from .manhuadb import ManHuaDB
        return ManHuaDB()
    elif manga_site_enum == MangaSiteEnum.ManHuaGui:
        from .manhuagui import ManHuaGui
        return ManHuaGui()
    elif manga_site_enum == MangaSiteEnum.ManHuaBei:
        from .manhuabei import ManHuaBei
        return ManHuaBei()
    elif manga_site_enum == MangaSiteEnum.ComicBus:
        from .comicbus import ComicBus
        return ComicBus()
    return ManHuaRen()


def get_idx_page(manga_site_enum: MangaSiteEnum, manga_page: str) -> str:
    site = get_manga_site(manga_site_enum)
    url = ""
    if manga_site_enum == MangaSiteEnum.ManHuaRen:
        url = f"{site.url}{manga_page.strip('/')}/"
    elif manga_site_enum == MangaSiteEnum.ManHuaDB:
        url = f"{site.url}manhua/{manga_page.strip('/')}/"
    elif manga_site_enum == MangaSiteEnum.ManHuaGui:
        url = f"{site.url}comic/{manga_page.strip('/')}/"
    elif manga_site_enum == MangaSiteEnum.ManHuaBei:
        url = f"{site.url}manhua/{manga_page.strip('/')}/"
    elif manga_site_enum == MangaSiteEnum.ComicBus:
        url = f"{site.url}html/{manga_page.strip('/')}/"
    return url
