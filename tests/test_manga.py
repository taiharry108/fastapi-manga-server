import unittest
from core.manga import Manga, MangaIndexTypeEnum
from core.chapter import Chapter

def get_sample_manga():
    manga_name = "Test Name"
    manga_url = "Test Url"
    return Manga(name=manga_name, url=manga_url)

class TestManga(unittest.TestCase):
    
    def setUp(self):
        self.manga = get_sample_manga()
        self.chapter_title = 'Test Title'
        self.chapter_page_url = "Test Page Url"

    def test_create_manga(self):
        """Test create manga"""
        manga = get_sample_manga()
        self.assertEqual(manga.name, "Test Name")
        self.assertEqual(manga.url, "Test Url")
        self.assertIsInstance(manga.chapters, dict)
        self.assertEqual(len(manga.chapters), 3)
        for chapter_list in manga.chapters.values():
            self.assertIsInstance(chapter_list, list)
            self.assertEqual(len(chapter_list), 0)
        self.assertIsNone(manga.last_update)
        self.assertIsNone(manga.is_finished)
        self.assertIsNone(manga.thum_img)
    
    def test_add_chapter(self):
        """Test add chapter method"""
        manga = self.manga        
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 0)
        manga.add_chapter(MangaIndexTypeEnum.CHAPTER,
                          self.chapter_title, self.chapter_page_url)
        self.assertEqual(len(manga.chapters[MangaIndexTypeEnum.CHAPTER]), 1)
    
    def test_get_chapter(self):
        """Test get chapter"""
        manga = self.manga
        manga.add_chapter(MangaIndexTypeEnum.CHAPTER,
                          self.chapter_title, self.chapter_page_url)
        chapter = manga.get_chapter(MangaIndexTypeEnum.CHAPTER, 0)
        self.assertEqual(chapter.title, self.chapter_title)
        self.assertEqual(chapter.page_url, self.chapter_page_url)


        
