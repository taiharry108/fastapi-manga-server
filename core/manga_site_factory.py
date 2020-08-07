from core.manhuadb import ManHuaDB
from core.manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manhuaren import ManHuaRen


def get_manga_site(manga_site_enum: MangaSiteEnum) -> MangaSite:
    if manga_site_enum == MangaSiteEnum.ManHuaRen:
        return ManHuaRen()
    elif manga_site_enum == MangaSiteEnum.ManHuaDB:
        return ManHuaDB()
    return ManHuaRen()


def get_idx_page(manga_site_enum: MangaSiteEnum, manga_page: str) -> str:
    site = get_manga_site(manga_site_enum)
    url = ""
    if manga_site_enum == MangaSiteEnum.ManHuaRen:
        url = f"{site.url}{manga_page.strip('/')}/"
    elif manga_site_enum == MangaSiteEnum.ManHuaDB:
        url = f"{site.url}manhua/{manga_page.strip('/')}/"
    return url