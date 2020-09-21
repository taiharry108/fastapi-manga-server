import aiohttp
from functools import wraps


def enter_session(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            await func(*args, session=session, **kwargs)
        return
    return wrapped
