# from core.manga_site import MangaSite
# from core.manga_site_enum import MangaSiteEnum
# import unittest


# class TestMangaSite(unittest.TestCase):
#     def test_create_manga_site(self):
#         """Test creating site"""
#         name = "Manga Site 1"
#         url = "Manga Url"
#         m_site = MangaSite(name, url)

#         self.assertEqual(m_site.name, name)
#         self.assertEqual(m_site.url, url)

#     def test_get_manga(self):
#         """Test get manga"""
#         name = "Manga Site 1"
#         url = "Manga Url"
#         m_site = MangaSite(name, url)

#         manga_name = "Manga Name"
#         manga_url = "Manga Url"
#         manga = m_site.get_manga(MangaSiteEnum.ManHuaRen, manga_name, manga_url)

#         self.assertEqual(manga.name, manga_name)
#         self.assertEqual(manga.url, manga_url)
