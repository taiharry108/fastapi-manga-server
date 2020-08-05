import aiohttp
from functools import wraps


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


def enter_session(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await func(*args, session=session, **kwargs)
    return wrapped
