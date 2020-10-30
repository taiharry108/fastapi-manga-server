from httpx import AsyncClient, Limits
SIZE_POOL_HTTPX = 5

limits = Limits(max_connections=20, max_keepalive_connections=20)

class SingletonHttpx(object):
    client: AsyncClient = None

    @classmethod
    def get_client(cls) -> AsyncClient:
        if cls.client is None or cls.client.is_closed:

            cls.client = AsyncClient(limits=limits, timeout=5)
            
        return cls.client

    @classmethod
    async def close_client(cls):        
        if cls.client:
            await cls.client.aclose()
            cls.client = None
