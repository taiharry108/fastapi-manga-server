import aiounittest
from core.manhuaren import ManHuaRen
from core.manga import MangaIndexTypeEnum
from core.downloader import Downloader
from core.utils import enter_session
import json

class TestManHuaRen(aiounittest.AsyncTestCase):
    def setUp(self):
        self.downloader = Downloader(None)
        self.site = ManHuaRen()

    @enter_session
    async def test_search_manga1(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者":
                self.assertTrue(manga.url.endswith("manhua-huoyingrenzhe-naruto/"))

    @enter_session
    async def test_search_manga2(self, session):
        self.downloader.session = session
        manga_list = await self.site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE":
                self.assertTrue(manga.url.endswith("manhua-dr-stone/"))

    @enter_session
    async def test_get_index_page(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuaren.com/manhua-huoyingrenzhe-naruto/")
        self.assertEqual(manga.name, "火影忍者")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 521)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 20)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        self.assertTrue(chap.page_url.endswith("m208255/"))
        self.assertEqual(chap.title, '第710话')
    
    @enter_session
    async def test_get_index_page1(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuaren.com/manhua-haidaozhanji/")
        self.assertEqual(manga.name, "海盗战记")
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 130)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.MISC]), 1)

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        self.assertTrue(chap.page_url.endswith("m1006905/"))
        self.assertEqual(chap.title, '第169话')
    
    @enter_session
    async def test_get_page_urls(self, session):
        self.downloader.session = session
        manga = await self.site.get_index_page("https://www.manhuaren.com/manhua-haidaozhanji/")
        img_urls = await self.site.get_page_urls(manga, MangaIndexTypeEnum.CHAPTER, 0)
        self.assertEqual(len(img_urls), 24)
        self.assertTrue(
            img_urls[0].startswith("https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/1_1002.jpg?cid=1006905"))
        self.assertTrue(
            img_urls[-1].startswith("https://manhua1034-104-250-139-219.cdnmanhua.net/3/2800/1006905/24_5981.jpg?cid=1006905"))
    
    @enter_session
    async def test_download_chapter(self, session):
        self.downloader.session = session
        count = 0
        manga = await self.site.get_index_page("https://www.manhuaren.com/manhua-haidaozhanji/")        
        async for item_str in self.site.download_chapter(manga, MangaIndexTypeEnum.CHAPTER, 0):            
            item = json.loads(item_str[6:-2])
            if len(item) == 0:
                continue
            idx = item['idx']
            image_bytes = item['message']
            count += 1
            if idx == 0:
                self.assertEqual(len(image_bytes), 442088)
            
        self.assertEqual(count, 24)





