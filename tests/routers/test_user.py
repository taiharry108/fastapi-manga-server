from database import models
from database.crud import user_crud
from database.crud import utils
from core.manga_site_enum import MangaSiteEnum
from database.crud import manga_crud, manga_site_crud
import unittest
from fastapi.testclient import TestClient
from fastapi import status
from starlette.config import Config

from main import app
from .test_database import override_get_db
from database.utils import get_db

config = Config('.env')

app.dependency_overrides[get_db] = override_get_db


class TestUserPrivate(unittest.TestCase):
    def setUp(self):
        self.db = next(override_get_db())
        utils.delete_all(self.db)
        manga_site_crud.create_test_manga_site(self.db)
        self.client = TestClient(app)
        response = self.client.post("/api/auth/login",
                                    headers={
                                        "X-Requested-With": "application/json"
                                    },
                                    data=config('TEST_AUTH_TOKEN')
                                    )
        self.code = response.headers['set-cookie'].split(
            '; ')[0].split('=')[1][1:-1]

    def create_manga(self) -> models.Manga:
        """Helper function to create test manga"""
        self.test_manga_name = 'test'
        self.test_manga_url = "https://test.com"
        return manga_crud.create_manga_with_manga_site_id(self.db, self.test_manga_name, self.test_manga_url, 1)

    def tearDown(self) -> None:
        # utils.delete_all(self.db)
        pass

    def test_me_success(self):
        """Test me with authorization"""
        response = self.client.get(
            "/api/user/me", cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_favs(self):
        """Test get favorites with auth"""
        response = self.client.get(
            '/api/user/favs', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())

    def test_add_fav_failed(self):
        """Test add fav failed"""
        response = self.client.post(
            '/api/user/add_fav/1', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.json()['success'])

    def test_add_fav_successful(self):
        """Test add fav successful"""
        self.create_manga()
        
        response = self.client.post(
            '/api/user/add_fav/1', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])

        response = self.client.get(
            '/api/user/favs', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], self.test_manga_name)
        self.assertEqual(result[0]['url'], self.test_manga_url)

    def test_add_fav_twice_failed(self):
        """Test add fav successful"""
        self.create_manga()

        response = self.client.post(
            '/api/user/add_fav/1', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.json()['success'])

        response = self.client.post(
            '/api/user/add_fav/1', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.json()['success'])

        response = self.client.get(
            '/api/user/favs', cookies={"Authorization": self.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], self.test_manga_name)
        self.assertEqual(result[0]['url'], self.test_manga_url)

    def test_del_fav_successful(self):
        """Test del fav successful"""
        manga = self.create_manga()
        user = user_crud.get_users(self.db)[0]
        self.assertEqual(user.id, 1)
        success = user_crud.add_fav_manga(self.db, manga.id, user.id)
        self.assertTrue(success)
        response = self.client.delete(
            '/api/user/del_fav/1', cookies={"Authorization": self.code})

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(response.json()['success'])

    def test_del_fav_failed(self):
        """Test del fav failed"""
        user = user_crud.get_users(self.db)[0]
        self.assertEqual(user.id, 1)
        response = self.client.delete(
            '/api/user/del_fav/1', cookies={"Authorization": self.code})

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertFalse(response.json()['success'])


class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_me_failed(self):
        """Test me without authorization"""
        response = self.client.get("/api/user/me")
        self.assertEqual(response.status_code, 403)

    def test_get_favs(self):
        """Test get favorites without authorization"""
        response = self.client.get("/api/user/favs")
        self.assertEqual(response.status_code, 403)
