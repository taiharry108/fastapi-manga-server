import asyncio
import base64
from pathlib import Path
from typing import Any, AsyncIterable, Callable, Dict, List, Union
import uuid
from bs4 import BeautifulSoup
from pydantic import HttpUrl
from .singleton_httpx import SingletonHttpx
from functools import wraps
from httpx import Response

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6,zh-CN;q=0.5'
}

def get_resp(func: Callable) -> Callable:
    @wraps(func)
    async def wrapped(self: "Downloader", url: HttpUrl, additional_headers: Dict[str, str] = {}, **kwargs):
        headers = {}
        headers.update(additional_headers)
        headers.update(HEADERS)

        resp = await self.client.get(url, headers=headers)
        
        if resp.status_code == 200:            
            return await func(self, resp, **kwargs)
        else:
            raise RuntimeError(f"response status code: {resp.status_code}")
    return wrapped

class Downloader(object):
    def __init__(self):
        self.num_workers = 2
        self.download_dir = Path('./static/images')
        self.client = SingletonHttpx.get_client()
    
    @get_resp
    async def get_json(self, resp: Response) -> Union[List, Dict]:
        """Make a get request and return with BeautifulSoup"""
        return resp.json()
    
    @get_resp
    async def get_soup(self, resp: Response) -> BeautifulSoup:
        """Make a get request and return with BeautifulSoup"""
        return BeautifulSoup(resp.text, features='html.parser')
    
    @get_resp
    async def get_byte_soup(self, resp: Response) -> BeautifulSoup:
        """Make a get request and return with BeautifulSoup"""
        return BeautifulSoup(resp.content, features="html.parser")
    
    @get_resp
    async def get_img(self, resp: Response, download: bool = False, download_path: Path = None) -> Union[bytes, str]:
        b = resp.content
        if not download: return b
        
        content_type = resp.headers['content-type']
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
            raise RuntimeError("Response is not an image")
    
    async def _producer(self, in_q: asyncio.Queue, out_q: asyncio.Queue, referer: HttpUrl, download_path: Path = None):
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
    
    async def get_images(self, urls: List[str], referer: str, download_path: Path) -> AsyncIterable[Dict[str, Any]]:
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
        
