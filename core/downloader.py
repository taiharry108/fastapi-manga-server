from bs4 import BeautifulSoup
import aiohttp
from typing import Any, AsyncIterable, Dict, List

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6,zh-CN;q=0.5'
}


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance == None:
            self.instance = self.klass(*args, **kwargs)
        return self.instance


class _Downloader(object):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_soup(self, url: str) -> BeautifulSoup:
        """Make a get request and return with BeautifulSoup"""        
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return BeautifulSoup(await resp.text(), features="html.parser")
            else:
                raise RuntimeError(f"response status code: {resp.status}")

    async def get_img(self, url: str) -> bytes:
        """Request image and return with bytes"""
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                while True:
                    return await resp.content.read()
            else:
                raise RuntimeError(f"response status code: {resp.status}")
        
    async def get_images(self, urls: List[str]) -> AsyncIterable[Dict[str, Any]]:
        for idx, url in enumerate(urls):
            img_bytes = await self.get_img(url)
            yield {"idx": idx, "img": img_bytes}


Downloader = SingletonDecorator(_Downloader)
