import aiounittest
from core.comicbus import ComicBus
from core.manga import MangaIndexTypeEnum
from core.downloader import Downloader
from core.utils import enter_session
import json


class TestComicBus(aiounittest.AsyncTestCase):
    def setUp(self):
        self.downloader = Downloader(None)
        self.site = ComicBus()

    @enter_session
    async def test_search_manga1(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("stone")
        found = False
        for manga in manga_list:
            if manga.name.upper() == "DR.STONE":
                found = True
                self.assertTrue(manga.url.endswith(
                    "html/14898.html/"))
        self.assertTrue(found)

    @enter_session
    async def test_search_manga2(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("火影")
        found = False
        for manga in manga_list:
            if manga.name == "火影忍者":
                found = True
                self.assertTrue(manga.url.endswith("html/102.html/"))
        self.assertTrue(found)

    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://comicbus.com/html/102.html")
        self.assertEqual(manga.name, "火影忍者")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.VOLUME]), 58)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 342)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 0)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        self.assertTrue(chap.page_url.endswith("a-102.html?ch=370"))
        self.assertEqual(chap.title, '370話 不安')
    
    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://comicbus.com/html/3997.html")
        self.assertEqual(manga.name, "海盜戰記")

    
    @enter_session
    async def test_get_page_urls(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://comicbus.com/html/102.html/")
        img_urls = await self.site.get_page_urls(manga, MangaIndexTypeEnum.CHAPTER, 0)
        self.assertEqual(len(img_urls), 16)
        self.assertEqual(
            img_urls[0], "https://img8.8comic.com/2/102/370/001_Ma5.jpg")
        self.assertEqual(
            img_urls[-1], "https://img8.8comic.com/2/102/370/016_VS3.jpg")

    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://comicbus.com/html/102.html/")
        async for item_str in self.site.download_chapter(manga, MangaIndexTypeEnum.CHAPTER, 0):
            item = json.loads(item_str[6:-2])
            if len(item) == 0:
                continue
            idx = item['idx']
            image_bytes = item['message']
            count += 1
            if idx == 0:
                self.assertEqual(len(image_bytes), 228108)

        self.assertEqual(count, 16)
