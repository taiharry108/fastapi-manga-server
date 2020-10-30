
from core.manga_site import MangaSite
import pytest
from core.manhuadb import ManHuaDB
from core.manga import MangaIndexTypeEnum


@pytest.fixture(scope='class')
def site(downloader) -> MangaSite:
    site = ManHuaDB()
    site.downloader = downloader
    return site



class TestManHuaDB:
    @pytest.mark.asyncio
    async def test_search_manga1(self, site: ManHuaDB):        
        manga_list = await site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者第一话复制原稿BOX":
                assert manga.url.endswith("manhua/22315/")

    @pytest.mark.asyncio
    async def test_search_manga2(self, site: ManHuaDB):
        manga_list = await site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE 新石纪":
                assert manga.url.endswith("manhua/1408/")

    @pytest.mark.asyncio
    async def test_get_index_page(self, site: ManHuaDB):
        manga = await site.get_index_page("https://www.manhuadb.com/manhua/136")
        assert manga.name == "火影忍者 NARUTO"
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) == 72
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) == 0

        chap = manga.get_chapter(
            MangaIndexTypeEnum.VOLUME, 0)
        assert chap.page_url.endswith("manhua/136/55_458.html")
        assert chap.title == '01'

    @pytest.mark.asyncio
    async def test_get_index_page1(self, site: ManHuaDB):
        manga = await site.get_index_page("https://www.manhuadb.com/manhua/2661")
        assert manga.name == "海盗战记"
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) == 13
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) == 1

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)        
        assert chap.page_url.endswith("manhua/2661/3283_59202.html")
        assert chap.title == '第072回'

    @pytest.mark.asyncio
    async def test_get_page_urls(self, site: ManHuaDB):
        manga = await site.get_index_page("https://www.manhuadb.com/manhua/2661")
        img_urls = await site.get_page_urls(manga, "https://www.manhuadb.com/manhua/2661/3283_59202.html")
        assert len(img_urls) == 30
        assert img_urls[0] == "https://i1.manhuadb.com/ccbaike/3283/59202/1_lavotadu.webp"
        assert img_urls[-1] == "https://i1.manhuadb.com/ccbaike/3283/59202/30_rmggegzv.webp"

    @pytest.mark.asyncio
    async def test_download_chapter(self, site: ManHuaDB):
        count = 0
        manga = await site.get_index_page("https://www.manhuadb.com/manhua/2661")
        async for item in site.download_chapter(manga, "https://www.manhuadb.com/manhua/2661/3283_59202.html"):
            assert "idx" in item
            assert "pic_path" in item
            count += 1
        assert count == 30
