from database.crud import manga_crud
from database.utils import get_db
from .test_database import override_get_db
from main import app
import unittest
from fastapi.testclient import TestClient
from starlette.config import Config



config = Config('.env')

app.dependency_overrides[get_db] = override_get_db


class TestMain(unittest.TestCase):
    def setUp(self):
        self.db = next(override_get_db())

    def test_search_manga(self):
        """Test search manga on MHR"""
        with TestClient(app) as client:

            response = client.get("/api/search/manhuaren/火影")
            results = response.json()
            self.assertEqual(response.status_code, 200)
            for manga in results:
                # self.assertIsNotNone(manga['id'])
                if manga['name'] == '火影忍者':
                    url = manga['url']
                    self.assertEqual(
                        url, 'https://www.manhuaren.com/manhua-huoyingrenzhe-naruto/')

                    db_manga = manga_crud.get_manga_by_url(self.db, url)

                    self.assertIsNotNone(db_manga)
                    self.assertEqual(db_manga.name, manga['name'])

    def test_get_index(self):
        """Test get index on MHR"""
        with TestClient(app) as client:
            response = client.get(
                "/api/index/manhuaren/manhua-huoyingrenzhe-naruto")
            result = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['name'], '火影忍者')
            self.assertEqual(result['finished'], True)
            self.assertIsNotNone(result['id'])

    def test_get_chapter(self):
        """Test get chapter on MHR"""
        with TestClient(app) as client:
            response = client.get(
                "/api/chapter/manhuaren/manhua-huoyingrenzhe-naruto", params={'idx': 0})
            self.assertEqual(response.status_code, 200)
