import aiounittest
from core.comicbus import ComicBus
from core.manga import MangaIndexTypeEnum
from core.utils import enter_session
import json


class TestComicBus(aiounittest.AsyncTestCase):
    def setUp(self):
        self.site = ComicBus()
        self.downloader = self.site.downloader        
        self.downloader.download_dir = Path("./static/test_images")

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
        img_urls = await self.site.get_page_urls(manga, "https://comicbus.live/online/a-102.html?ch=8001")
        self.assertEqual(len(img_urls), 44)
        self.assertEqual(
            img_urls[0], "https://img8.8comic.com/2/102/8001/001_my5.jpg")
        self.assertEqual(
            img_urls[-1].lower(), "https://img8.8comic.com/2/102/8001/044_Sf8.jpg".lower())

    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://comicbus.com/html/102.html/")
        async for item in self.site.download_chapter(manga, "https://comicbus.live/online/a-102.html?ch=8001"):
            self.assertTrue("idx" in item)
            self.assertTrue("pic_path" in item)
            count += 1
        self.assertEqual(count, 44)
