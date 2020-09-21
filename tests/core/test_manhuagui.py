import aiounittest
from core.manhuagui import ManHuaGui
from core.manga import MangaIndexTypeEnum
from core.downloader import Downloader
from core.utils import enter_session
import json

class TestManHuaGui(aiounittest.AsyncTestCase):
    def setUp(self):
        self.site = ManHuaGui()
        self.downloader = self.site.downloader

    @enter_session
    async def test_search_manga1(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者":
                self.assertTrue(manga.url.endswith("comic/4681/"))

    @enter_session
    async def test_search_manga2(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE":
                self.assertTrue(manga.url.endswith("comic/23270/"))

    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuagui.com/comic/23270/")
        self.assertEqual(manga.name, "Dr.STONE")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.VOLUME]), 9)
        self.assertTrue(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) >= 164)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 2)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        self.assertTrue(chap.page_url.endswith("comic/23270/290296.html"))
        self.assertEqual(chap.title, '第01回')

        chap2 = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 163)
        self.assertTrue(chap2.page_url.endswith("comic/23270/511656.html"))
        self.assertEqual(chap2.title, '第160话 试看版')


    @enter_session
    async def test_get_page_urls(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuagui.com/comic/23270/")
        img_urls = await self.site.get_page_urls(manga, "https://www.manhuagui.com/comic/23270/511656.html")
        self.assertEqual(len(img_urls), 19)

    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://www.manhuagui.com/comic/23270/")
        async for item_str in self.site.download_chapter(manga, "https://www.manhuagui.com/comic/23270/511656.html"):
            item = json.loads(item_str[6:-2])
            if len(item) == 0:
                continue
            idx = item['idx']
            image_bytes = item['message']
            count += 1
            if idx == 0:
                self.assertTrue(len(image_bytes) > 100000)

        self.assertEqual(count, 19)
