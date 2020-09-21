import aiounittest
from core.manhuabei import ManHuaBei
from core.manga import MangaIndexTypeEnum
from core.downloader import Downloader
from core.utils import enter_session
import json


class TestManHuaBei(aiounittest.AsyncTestCase):
    def setUp(self):        
        self.site = ManHuaBei()
        self.downloader = self.site.downloader

    
    @enter_session
    async def test_get_img_domain(self, session):
        self.downloader.session = session
        img_domain = await self.site.get_img_domain()
        self.assertEqual(img_domain.startswith("https://"))

    @enter_session
    async def test_search_manga1(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("鬼滅")
        for manga in manga_list:
            if manga.name == "鬼灭之刃":
                self.assertTrue(manga.url.endswith(
                    "manhua/guimiezhiren/"))

    @enter_session
    async def test_search_manga2(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE 石纪元":
                self.assertTrue(manga.url.endswith(
                    "manhua/DrSTONE/"))

    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuabei.com/manhua/haizeiwang/")
        self.assertEqual(manga.name, "海贼王")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 549)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.VOLUME]), 42)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 21)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.VOLUME, 0)
        
        self.assertTrue(chap.page_url.endswith(
            "manhua/haizeiwang/68856.html"))
        self.assertEqual(chap.title, '01卷')

    
    @enter_session
    async def test_get_page_urls(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuabei.com/manhua/haizeiwang/")
        img_urls = await self.site.get_page_urls(manga, MangaIndexTypeEnum.CHAPTER, 0)
        self.assertEqual(len(img_urls), 7)

    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://www.manhuabei.com/manhua/haizeiwang/")
        async for item_str in self.site.download_chapter(manga, MangaIndexTypeEnum.CHAPTER, 0):
            item = json.loads(item_str[6:-2])
            if len(item) == 0:
                continue
            idx = item['idx']
            image_bytes = item['message']
            count += 1
            if idx == 0:
                self.assertEqual(len(image_bytes), 423860)

        self.assertEqual(count, 7)
