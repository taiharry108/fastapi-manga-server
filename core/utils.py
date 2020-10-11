from core.manga_site_factory import get_manga_site
from core.manga_site import MangaSite
from core.manga_site_enum import MangaSiteEnum
import aiohttp
from functools import wraps


def enter_session(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            await func(*args, session=session, **kwargs)
        return
    return wrapped


async def is_test() -> bool:
    return False


async def get_manga_site_common(site: MangaSiteEnum) -> MangaSite:
    return get_manga_site(site)