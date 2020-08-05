from bs4 import BeautifulSoup
import aiohttp
import asyncio
from typing import Any, AsyncIterable, Dict, List
from core.utils import SingletonDecorator

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6,zh-CN;q=0.5'
}

@SingletonDecorator
class Downloader(object):
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.num_workers = 2

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
        """Request images and return async iterable dictionary with image bytes and index"""
        async def producer(in_q, out_q):
            while True:
                item = await in_q.get()

                if item is None:
                    await in_q.put(None)
                    await out_q.put(None)
                    break
                idx, url = item
                img_bytes = await self.get_img(url)
                await asyncio.sleep(0.3)
                await out_q.put((idx, img_bytes))

        async def consumer(q):
            count = 0
            while True:
                item = await q.get()

                if item is None:
                    count += 1
                else:
                    yield item
                if count == self.num_workers:
                    break

        prod_queue = asyncio.Queue()
        con_queue = asyncio.Queue()
        for idx, url in enumerate(urls):
            await prod_queue.put((idx, url))
        await prod_queue.put(None)

        [asyncio.create_task(
            producer(prod_queue, con_queue)) for i in range(self.num_workers)]

        async for idx, img_bytes in consumer(con_queue):
            yield {"idx": idx, "img": img_bytes}
