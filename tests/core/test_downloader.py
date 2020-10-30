from pathlib import Path
from core.downloader import Downloader
import pytest


class TestDownloader:
    @pytest.mark.asyncio
    async def test_get_soup(self, downloader: Downloader):
        soup = await downloader.get_soup("https://www.example.com")
        h1_text = soup.find("h1").text
        assert h1_text == "Example Domain"

    @pytest.mark.asyncio
    async def test_get_soup_error(self, downloader: Downloader):
        with pytest.raises(RuntimeError) as e:
            soup = await downloader.get_soup("https://www.example.com/fdsafsda")
            assert "response status code" in e.value

    @pytest.mark.asyncio
    async def test_get_image(self, downloader: Downloader):
        img_bytes = await downloader.get_img(
            "https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1")
        assert len(img_bytes) == 331566
        assert isinstance(img_bytes, bytes)

    @pytest.mark.asyncio
    async def test_get_image_download(self, downloader: Downloader):
        img_path = await downloader.get_img(
            "https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1",
            download=True, download_path=Path('test'))
        assert isinstance(img_path, str)
        assert 'test' in img_path

    @pytest.mark.asyncio
    async def test_get_chapter_images(self, downloader: Downloader):
        count = 0
        urls = ["https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1",
                "https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/2_7528.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1"]
        async for img_dict in downloader.get_images(urls, "", download_path=Path('test')):
            count += 1
            print(img_dict['idx'])
            assert 'pic_path' in img_dict
            assert 'idx' in img_dict
        assert count == 2
