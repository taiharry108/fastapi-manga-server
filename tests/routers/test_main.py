from database.crud import chapter_crud
from core.utils import get_manga_site_common, is_test
from database.crud import manga_site_crud
from database.crud import utils
from database.crud import manga_crud
from database.utils import get_db
from .utils import override_get_db, override_get_manga_site_common, override_is_test
from main import app
import unittest
from fastapi.testclient import TestClient
from starlette.config import Config
import json


config = Config('.env')

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[is_test] = override_is_test
app.dependency_overrides[get_manga_site_common] = override_get_manga_site_common


class TestMain(unittest.TestCase):
    def setUp(self):
        self.db = next(override_get_db())
        utils.delete_all(self.db)
        manga_site_crud.create_test_manga_site(self.db)

    def test_search_manga(self):
        """Test search manga on MHR"""
        with TestClient(app) as client:

            response = client.get("/api/search/manhuaren/火影")
            results = response.json()
            self.assertEqual(response.status_code, 200)
            for manga in results:
                self.assertIsNotNone(manga['id'])
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
            client.get("/api/search/manhuaren/火影")
            response = client.get(
                "/api/index/manhuaren/1")
            result = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(result['name'], '火影忍者')
            self.assertEqual(result['finished'], True)
            self.assertIsNotNone(result['id'])

    
    def test_get_chapter(self):
        """Test get chapter on MHR"""
        page_url = "https://www.manhuaren.com/m424056/"
        with TestClient(app) as client:
            response = client.get("/api/search/manhuaren/海盜")
            manga_id = None
            for manga in response.json():
                if 'manhua-haidaozhanji' in manga['url']:
                    manga_id = manga['id']
            self.assertIsNotNone(manga_id)
            
            client.get(
                f'/api/index/manhuaren/{manga_id}')
            
            response = client.get(
                f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
            self.assertEqual(response.status_code, 200)            
            
            content = response.content.decode()
            results = [json.loads(item_str[6:]) for item_str in content.split('\n\n')[:-2]]
            self.assertEqual(len(results), 8)
            for item in results:
                self.assertTrue("idx" in item)
                self.assertTrue("total" in item)
                self.assertTrue("pic_path" in item)
            
            db_pages = chapter_crud.get_chapter_pages(self.db, page_url)
            self.assertEqual(len(db_pages), 8)
        
    def test_get_chapter_twice(self):
        """Test get chapter twice on MHR get same result"""
        page_url = "https://www.manhuaren.com/m424056/"
        with TestClient(app) as client:
            response = client.get("/api/search/manhuaren/海盜")
            manga_id = None
            for manga in response.json():
                if 'manhua-haidaozhanji' in manga['url']:
                    manga_id = manga['id']
            self.assertIsNotNone(manga_id)
            
            client.get(
                f'/api/index/manhuaren/{manga_id}')
            response = client.get(
                f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
            response2 = client.get(
                f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
            self.assertEqual(response.status_code, 200)

            content = response.content.decode()
            results = [json.loads(item_str[6:])
                       for item_str in content.split('\n\n')[:-2]]
            
            content2 = response2.content.decode()
            results2 = [json.loads(item_str[6:])
                       for item_str in content2.split('\n\n')[:-2]]
            
            result_dict = {item['idx']: item for item in results}
            for item in results2:
                self.assertEqual(result_dict[item['idx']], item)
