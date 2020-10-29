# import unittest
from datetime import datetime
from typing import Dict
from core.manga_site_enum import MangaSiteEnum
from core.manga import Manga, MangaBase, MangaIndexTypeEnum, MangaWithMeta
from core.chapter import Chapter
import pytest


@pytest.fixture
def manga_base() -> MangaBase:
    name = 'Test Name'
    url = 'https://www.test.com'
    site = MangaSiteEnum.ManHuaRen
    return MangaBase(name=name, url=url, site=site)


@pytest.fixture
def manga_with_meta(manga_base) -> MangaWithMeta:
    return MangaWithMeta(**manga_base.dict())


@pytest.fixture
def manga(manga_with_meta) -> Manga:
    return Manga(**manga_with_meta.dict())


@pytest.fixture
def chapter() -> Chapter:
    title = 'Test Title'
    page_url = 'https://www.testchap.com'
    return Chapter(title=title, page_url=page_url)


class TestMangaWithMeta:
    def test_retreived_idx_page(self, manga_with_meta: MangaWithMeta):
        manga_with_meta.retreived_idx_page()
        assert manga_with_meta.idx_retrieved

    def test_set_meta_data(self, manga_with_meta: MangaWithMeta):
        thum_img = 'images/test.jpg'
        manga_with_meta.set_meta_data({
            'finished': True,
            'thum_img': thum_img
        })

        assert manga_with_meta.thum_img == thum_img
        assert manga_with_meta.finished
        assert manga_with_meta.last_update <= datetime.now()


class TestManga:
    def test_manga(self, manga: Manga):
        assert hasattr(manga, 'chapters')
        assert isinstance(manga.chapters, dict)
        assert len(manga.chapters) == len(MangaIndexTypeEnum)
        assert isinstance(manga.chapters[MangaIndexTypeEnum.CHAPTER], list)

    def test_add_chapter(self, manga: Manga, chapter: Chapter):
        m_type = MangaIndexTypeEnum.CHAPTER
        manga.add_chapter(m_type, title=chapter.title, page_url=chapter.page_url)

        assert len(manga.chapters[m_type]) == 1
        assert manga.chapters[m_type][0].title == chapter.title
        assert manga.chapters[m_type][0].page_url == chapter.page_url

    def test_get_chapter(self, manga: Manga, chapter: Chapter):
        m_type = MangaIndexTypeEnum.CHAPTER
        manga.add_chapter(m_type, title=chapter.title,
                          page_url=chapter.page_url)
        assert manga.get_chapter(m_type, 0) == chapter