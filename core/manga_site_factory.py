from core.manga_site import MangaSite
from .manga_site_enum import MangaSiteEnum
from .manhuaren import ManHuaRen


def get_manga_site(manga_site_enum: MangaSiteEnum) -> MangaSite:
    if manga_site_enum == MangaSiteEnum.ManHuaRen:
        return ManHuaRen()
    return ManHuaRen()
