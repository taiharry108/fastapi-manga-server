from core.manga_site import MangaSite
import pytest
from core.manhuagui import ManHuaGui
from core.manga import MangaIndexTypeEnum


@pytest.fixture(scope='class')
def site(downloader) -> MangaSite:
    site = ManHuaGui()
    site.downloader = downloader
    return site


class TestManHuaGui:
    @pytest.mark.asyncio
    async def test_search_manga1(self, site: ManHuaGui):
        manga_list = await site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者":
                assert manga.url.endswith("comic/4681/")

    @pytest.mark.asyncio
    async def test_search_manga2(self, site: ManHuaGui):
        manga_list = await site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE":
                assert manga.url.endswith("comic/23270/")

    @pytest.mark.asyncio
    async def test_get_index_page(self, site: ManHuaGui):
        manga = await site.get_index_page("https://www.manhuagui.com/comic/23270/")

        assert manga.name == "Dr.STONE"
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) >= 164
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) >= 2
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) >= 9

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        assert chap.page_url.endswith("comic/23270/290296.html")
        assert chap.title == '第01回'

        chap2 = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 163)
        assert chap2.page_url.endswith("comic/23270/511656.html")
        assert chap2.title == '第160话 试看版'

    @pytest.mark.asyncio
    async def test_get_page_urls(self, site: ManHuaGui):
        manga = await site.get_index_page("https://www.manhuagui.com/comic/23270/")
        img_urls = await site.get_page_urls(manga, "https://www.manhuagui.com/comic/23270/511656.html")
        assert len(img_urls) == 19

    @pytest.mark.asyncio
    async def test_download_chapter(self, site: ManHuaGui):
        count = 0
        manga = await site.get_index_page("https://www.manhuagui.com/comic/23270/")
        async for item in site.download_chapter(manga, "https://www.manhuagui.com/comic/23270/511656.html"):
            assert "idx" in item
            assert "pic_path" in item
            count += 1
        assert count == 19
