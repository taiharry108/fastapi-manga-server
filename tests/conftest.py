from pathlib import Path
from core.singleton_httpx import SingletonHttpx
from core.downloader_factory import DownloaderFactory
from core.downloader import Downloader
import pytest
import asyncio

@pytest.fixture(scope="package")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='package')
async def downloader() -> Downloader:
    print('getting downloader here')
    downloader = DownloaderFactory.get_downloader("test")
    downloader.download_dir = Path('./static/test_images')
    yield downloader
    print('cleaning up')
    await SingletonHttpx.close_client()
