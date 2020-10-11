import base64
from functools import wraps
from aiohttp.client_reqrep import ClientResponse
from bs4 import BeautifulSoup
import asyncio
from typing import Any, AsyncIterable, Callable, Dict, List, Union
from pathlib import Path
import uuid
from core.singleton_aiohttp import SingletonAiohttp

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


class Downloader(object):

    def __init__(self):
        self.session = SingletonAiohttp.get_session()
        self.num_workers = 2
        self.download_dir = Path('./static/images')

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
    async def get_img(self, resp: ClientResponse, download: bool =  False, download_path: Path = None) -> Union[bytes, str]:
        b = await resp.content.read()
        if download:
            content_type = resp.content_type
            if content_type.startswith('image'):
                dir_path = self.download_dir
                if download_path is not None:
                    dir_path /= download_path
                
                dir_path.mkdir(exist_ok=True, parents=True)
                file_path = dir_path / \
                    f'{uuid.uuid4()}.{content_type.split("/")[-1]}'
                with open(file_path, 'wb') as img_f:
                    img_f.write(b)
                return str(file_path)

            else:
                return b
        else:
            return b
        
    async def _producer(self, in_q: asyncio.Queue, out_q: asyncio.Queue, referer: str, download_path: Path = None):
        while True:
            item = await in_q.get()

            if item is None:
                await in_q.put(None)
                await out_q.put(None)
                break
            idx, url = item
            additional_headers = {
                "Referer": referer} if referer is not None else {}
            img_bytes = await self.get_img(url, additional_headers, download=True, download_path=download_path)
            await asyncio.sleep(0.3)
            await out_q.put((idx, img_bytes))
    
    async def _consumer(self, q: asyncio.Queue):
        count = 0
        while True:
            item = await q.get()

            if item is None:
                count += 1
            else:
                yield item
            if count == self.num_workers:
                break

    async def get_images(self, urls: List[str], referer: str, download_path=None) -> AsyncIterable[Dict[str, Any]]:
        """Request images and return async iterable dictionary with image bytes and index"""

        prod_queue = asyncio.Queue()
        con_queue = asyncio.Queue()
        total = len(urls)
        for idx, url in enumerate(urls):
            await prod_queue.put((idx, url))
        await prod_queue.put(None)

        [asyncio.create_task(
            self._producer(prod_queue, con_queue, referer, download_path=download_path)) for _ in range(self.num_workers)]
        
        async for idx, img_bytes in self._consumer(con_queue):
            if download_path is None:
                encoded_str = base64.b64encode(img_bytes).decode("utf-8")
                yield {"idx": idx, "message": encoded_str, "total": total}
            else:
                yield {"idx": idx, "pic_path": img_bytes, "total": total}


# Downloader = SingletonDecorator(_Downloader)
