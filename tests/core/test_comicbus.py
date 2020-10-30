
from core.manga_site import MangaSite
import pytest
from core.comicbus import ComicBus
from core.manga import MangaIndexTypeEnum


@pytest.fixture(scope='class')
def site(downloader) -> MangaSite:
    site = ComicBus()
    site.downloader = downloader
    return site


class TestComicBus:
    @pytest.mark.asyncio
    async def test_search_manga1(self, site: ComicBus):        
        manga_list = await site.search_manga("stone")
        found = False
        for manga in manga_list:
            if manga.name.upper() == "DR.STONE":
                found = True
                assert manga.url.endswith("html/14898.html/")
        assert found

    @pytest.mark.asyncio
    async def test_search_manga2(self, site: ComicBus):
        manga_list = await site.search_manga("火影")
        found = False
        for manga in manga_list:
            if manga.name == "火影忍者":
                found = True
                assert manga.url.endswith("html/102.html/")
        assert found

    @pytest.mark.asyncio
    async def test_get_index_page(self, site: ComicBus):
        manga = await site.get_index_page("https://comicbus.com/html/102.html")
        assert manga.name == "火影忍者"
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) == 58
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) == 342
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) == 0

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        assert chap.page_url.endswith("a-102.html?ch=370")
        assert chap.title == '370話 不安'
    
    @pytest.mark.asyncio
    async def test_get_index_page(self, site: ComicBus):
        manga = await site.get_index_page("https://comicbus.com/html/3997.html")
        assert manga.name == "海盜戰記"

    
    @pytest.mark.asyncio
    async def test_get_page_urls(self, site: ComicBus):
        manga = await site.get_index_page("https://comicbus.com/html/102.html/")
        img_urls = await site.get_page_urls(manga, "https://comicbus.live/online/a-102.html?ch=8001")
        assert len(img_urls) == 44
        assert img_urls[0].lower() == "https://img8.8comic.com/2/102/8001/001_my5.jpg".lower()
        assert img_urls[-1].lower() == "https://img8.8comic.com/2/102/8001/044_Sf8.jpg".lower()

    @pytest.mark.asyncio
    async def test_download_chapter(self, site: ComicBus):
        count = 0
        manga = await site.get_index_page("https://comicbus.com/html/102.html/")
        async for item in site.download_chapter(manga, "https://comicbus.live/online/a-102.html?ch=8001"):
            assert "idx" in item
            assert "pic_path" in item
            count += 1
        assert count == 44
