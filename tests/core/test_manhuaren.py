from core.manga_site import MangaSite
import pytest
from core.manhuaren import ManHuaRen
from core.manga import MangaIndexTypeEnum


@pytest.fixture(scope='class')
def site(downloader) -> MangaSite:
    site = ManHuaRen()
    site.downloader = downloader
    return site


class TestManHuaRen:
    @pytest.mark.asyncio
    async def test_search_manga1(self, site: ManHuaRen):
        manga_list = await site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者":
                assert manga.url.endswith(
                    "manhua-huoyingrenzhe-naruto/")

    @pytest.mark.asyncio
    async def test_search_manga2(self, site: ManHuaRen):
        manga_list = await site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE":
                assert manga.url.endswith("manhua-dr-stone/")

    @pytest.mark.asyncio
    async def test_get_index_page(self, site: ManHuaRen):
        manga = await site.get_index_page("https://www.manhuaren.com/manhua-huoyingrenzhe-naruto/")
        assert manga.name == "火影忍者"
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) == 521
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) == 20

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        assert chap.page_url.endswith("m5196/")
        assert chap.title == '第1卷'

    @pytest.mark.asyncio
    async def test_get_index_page1(self, site: ManHuaRen):
        manga = await site.get_index_page("https://www.manhuaren.com/manhua-haidaozhanji/")
        assert manga.name == "海盗战记"
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) == 130
        assert len(manga.chapters[MangaIndexTypeEnum.MISC]) == 1

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        assert chap.page_url.endswith("m32738/")
        assert chap.title, '第1卷'

    @pytest.mark.asyncio
    async def test_get_page_urls(self, site: ManHuaRen):
        manga = await site.get_index_page("https://www.manhuaren.com/manhua-haidaozhanji/")
        img_urls = await site.get_page_urls(manga, "https://www.manhuaren.com/m32738/")
        assert len(img_urls) == 99
        assert img_urls[0].startswith(
            "https://manhua1101-104-250-139-219.cdnmanhua.net/3/2800/32738/finaleden_001cz_60683891.jpg")

    @pytest.mark.asyncio
    async def test_download_chapter(self, site: ManHuaRen):
        count = 0
        manga = await site.get_index_page("https://www.manhuaren.com/manhua-paiqiu/")
        async for item in site.download_chapter(manga, "https://www.manhuaren.com/m117868/"):
            assert "idx" in item
            assert "pic_path" in item
            count += 1
        assert count == 15
