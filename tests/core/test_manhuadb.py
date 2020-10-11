import aiounittest
from core.manhuadb import ManHuaDB
from core.manga import MangaIndexTypeEnum
from core.downloader import Downloader
from core.utils import enter_session
import json


class TestManHuaDB(aiounittest.AsyncTestCase):
    def setUp(self):
        self.site = ManHuaDB()
        self.downloader = self.site.downloader
        self.downloader.download_dir = Path("./static/test_images")

    @enter_session
    async def test_search_manga1(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者第一话复制原稿BOX":
                self.assertTrue(manga.url.endswith("manhua/22315/"))

    @enter_session
    async def test_search_manga2(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE 新石纪":
                self.assertTrue(manga.url.endswith("manhua/1408/"))

    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuadb.com/manhua/136")
        self.assertEqual(manga.name, "火影忍者 NARUTO")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.VOLUME]), 72)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 0)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.VOLUME, 0)
        self.assertTrue(chap.page_url.endswith("manhua/136/55_458.html"))
        self.assertEqual(chap.title, '01')

    @enter_session
    async def test_get_index_page1(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuadb.com/manhua/2661")
        self.assertEqual(manga.name, "海盗战记")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.VOLUME]), 13)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 1)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)        
        self.assertTrue(chap.page_url.endswith("manhua/2661/3283_59202.html"))
        self.assertEqual(chap.title, '第072回')

    @enter_session
    async def test_get_page_urls(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuadb.com/manhua/2661")
        img_urls = await self.site.get_page_urls(manga, "https://www.manhuadb.com/manhua/2661/3283_59202.html")
        self.assertEqual(len(img_urls), 30)
        self.assertEqual(
            img_urls[0], "https://i1.manhuadb.com/ccbaike/3283/59202/1_lavotadu.webp")
        self.assertEqual(
            img_urls[-1], "https://i1.manhuadb.com/ccbaike/3283/59202/30_rmggegzv.webp")

    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://www.manhuadb.com/manhua/2661")
        async for item in self.site.download_chapter(manga, "https://www.manhuadb.com/manhua/2661/3283_59202.html"):
            self.assertTrue("idx" in item)
            self.assertTrue("pic_path" in item)
            count += 1
        self.assertEqual(count, 30)
