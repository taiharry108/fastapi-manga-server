from core.manga_site import MangaSite
import pytest
from core.copymanga import CopyManga
from core.manga import MangaIndexTypeEnum


@pytest.fixture(scope='class')
def site(downloader) -> MangaSite:
    site = CopyManga()
    site.downloader = downloader
    return site


class TestCopyManga:
    @pytest.mark.asyncio
    async def test_search_manga1(self, site: CopyManga):
        manga_list = await site.search_manga("火影")
        for manga in manga_list:
            if manga.name == "火影忍者":
                assert manga.url.endswith(
                    "comic/huoyingrenzhe")

    @pytest.mark.asyncio
    async def test_search_manga2(self, site: CopyManga):
        manga_list = await site.search_manga("stone")
        for manga in manga_list:
            if manga.name == "Dr.STONE":
                assert manga.url.endswith("comic/drstone")

    @pytest.mark.asyncio
    async def test_get_index_page(self, site: CopyManga):
        manga = await site.get_index_page("https://copymanga.net/comic/huoyingrenzhe")
        assert manga.name == "火影忍者"
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) == 11
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) == 72

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        print(chap.page_url)
        assert chap.page_url.endswith("1089aa80-c955-11e8-88c0-024352452ce0")
        assert chap.title == '第701话'

    @pytest.mark.asyncio
    async def test_get_index_page1(self, site: CopyManga):
        manga = await site.get_index_page("https://copymanga.net/comic/haidaozhanji")
        assert manga.name == "海盜戰記"
        assert len(manga.chapters[MangaIndexTypeEnum.CHAPTER]) >= 30
        assert len(manga.chapters[MangaIndexTypeEnum.VOLUME]) >= 20

        chap = manga.get_chapter(
            MangaIndexTypeEnum.CHAPTER, 0)
        assert chap.page_url.endswith("b1061004-a160-11ea-8370-024352452ce0")
        assert chap.title, '第145話'

    @pytest.mark.asyncio
    async def test_get_page_urls(self, site: CopyManga):
        manga = await site.get_index_page("https://copymanga.net/comic/huoyingrenzhe")
        img_urls = await site.get_page_urls(manga, "https://copymanga.net/comic/huoyingrenzhe/chapter/1089aa80-c955-11e8-88c0-024352452ce0")
        assert len(img_urls) == 24
        assert img_urls[0].startswith(
            "https://mirror.mangafunc.fun/comic/huoyingrenzhe/a5319/1089aa82-c955-11e8-88c0-024352452ce0.jpg")

    # @pytest.mark.asyncio
    # async def test_download_chapter(self, site: CopyManga):
    #     count = 0
    #     manga = await site.get_index_page("https://www.manhuaren.com/manhua-paiqiu/")
    #     async for item in site.download_chapter(manga, "https://www.manhuaren.com/m117868/"):
    #         assert "idx" in item
    #         assert "pic_path" in item
    #         count += 1
    #     assert count == 15
