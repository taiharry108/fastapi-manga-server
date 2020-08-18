import base64
from functools import wraps
from aiohttp.client_reqrep import ClientResponse
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from typing import Any, AsyncIterable, Callable, Dict, List, Tuple, Union
from core.utils import SingletonDecorator
from pathlib import Path
import uuid


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6,zh-CN;q=0.5'
}


def get_resp(func: Callable) -> Callable:
    @wraps(func)
    async def wrapped(self: "_Downloader", url: str, additional_headers: Dict[str, str] = {}, **kwargs):
        headers = {}
        headers.update(additional_headers)
        headers.update(HEADERS)
        async with self.session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await func(self, resp, **kwargs)
            else:
                raise RuntimeError(f"response status code: {resp.status}")
    return wrapped


class _Downloader(object):

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.num_workers = 2
        self.__download_dir = Path('./images')

    @get_resp
    async def get(self, resp: ClientResponse) -> str:
        """Make a get request and return with BeautifulSoup"""
        return await resp.text()

    @get_resp
    async def get_bytes(self, resp: ClientResponse) -> BeautifulSoup:
        """Make a get request and return with bytes"""
        return await resp.content.read()

    @get_resp
    async def get_byte_soup(self, resp: ClientResponse) -> BeautifulSoup:
        """Make a get request and return with BeautifulSoup"""
        return BeautifulSoup(await resp.content.read(), features="html.parser")

    @get_resp
    async def get_soup(self, resp: ClientResponse) -> BeautifulSoup:
        """Make a get request and return with BeautifulSoup"""
        return BeautifulSoup(await resp.text(), features="html.parser")

    @get_resp
    async def get_json(self, resp: ClientResponse) -> Any:
        """Make a get request and return with BeautifulSoup"""
        return await resp.json()

    @get_resp
    async def get_img(self, resp: ClientResponse, download: bool =  False) -> Union[bytes, str]:
        b = await resp.content.read()
        if download:
            content_type = resp.content_type
            if content_type.startswith('image'):
                file_path = self.__download_dir / \
                    f'{uuid.uuid4()}.{content_type.split("/")[-1]}'
                with open(file_path, 'wb') as img_f:
                    img_f.write(b)
                return str(file_path)

            else:
                return b
        else:
            return b

    async def get_images(self, urls: List[str], referer: str) -> AsyncIterable[Dict[str, Any]]:
        """Request images and return async iterable dictionary with image bytes and index"""
        async def producer(in_q, out_q):
            while True:
                item = await in_q.get()

                if item is None:
                    await in_q.put(None)
                    await out_q.put(None)
                    break
                idx, url = item
                print(referer)
                img_bytes = await self.get_img(url, {"Referer": referer})
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
        total = len(urls)
        for idx, url in enumerate(urls):
            await prod_queue.put((idx, url))
        await prod_queue.put(None)

        [asyncio.create_task(
            producer(prod_queue, con_queue)) for _ in range(self.num_workers)]

        async for idx, img_bytes in consumer(con_queue):
            encoded_str = base64.b64encode(img_bytes).decode("utf-8")
            yield {"idx": idx, "message": encoded_str, "total": total}


Downloader = SingletonDecorator(_Downloader)
