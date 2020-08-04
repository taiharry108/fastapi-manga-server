import aiounittest
from core.downloader import Downloader
import aiohttp


class TestDownloader(aiounittest.AsyncTestCase):
    def setUp(self):
        self.downloader = Downloader(None)

    async def test_get_soup(self):
        async with aiohttp.ClientSession() as session:
            self.downloader.session = session
            soup = await self.downloader.get_soup("https://www.example.com")
            h1_text = soup.find("h1").text
            self.assertEqual(h1_text, "Example Domain")

    async def test_get_soup_error(self):
        async with aiohttp.ClientSession() as session:
            self.downloader.session = session
            with self.assertRaises(RuntimeError) as e:
                await self.downloader.get_soup("http://www.example.com/testse")

    async def test_get_image(self):
        async with aiohttp.ClientSession() as session:
            self.downloader.session = session
            img_bytes = await self.downloader.get_img(
                "https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1")
            self.assertEqual(len(img_bytes), 331566)

    async def test_get_chapter_images(self):
        async with aiohttp.ClientSession() as session:
            self.downloader.session = session
            count = 0
            urls = ["https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1",
                    "https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/2_7528.jpg?cid=1006905&key=9a12f75785ef4d8dc9fffcfa58f5e406&type=1"]
            async for img_dict in self.downloader.get_images(urls):
                count += 1
                if img_dict["idx"] == 0:
                    self.assertEqual(len(img_dict["img"]), 331566)
            self.assertEqual(count, 2)
