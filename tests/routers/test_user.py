import unittest
from fastapi.testclient import TestClient
from fastapi import Cookie
from starlette.config import Config

from main import app
from .test_database import override_get_db
from database.utils import get_db

config = Config('.env')

app.dependency_overrides[get_db] = override_get_db


class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_public_me_failed(self):
        """Test me without authorization"""
        response = self.client.get("/api/user/me")
        self.assertEqual(response.status_code, 403)

    def test_private_me_success(self):
        response = self.client.post("/api/auth/login",
                                    headers={
                                        "X-Requested-With": "application/json"
                                    },
                                    data=config('TEST_AUTH_TOKEN')
                                    )
        code = response.headers['set-cookie'].split(
            '; ')[0].split('=')[1][1:-1]

        response = self.client.get(
            "/api/user/me", cookies={"Authorization": code})
        self.assertEqual(response.status_code, 200)
