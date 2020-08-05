import aiohttp
from socket import AF_INET

SIZE_POOL_AIOHTTP=5

class SingletonAiohttp(object):
    session: aiohttp.ClientSession = None

    @classmethod
    def get_session(cls) -> aiohttp.ClientSession:
        if cls.session is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)

            cls.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return cls.session
    
    @classmethod
    async def close_aiohttp_client(cls):
        if cls.session:
            await cls.session.close()
            cls.session = None
