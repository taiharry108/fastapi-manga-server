from typing import List
from database.crud.crud_enum import CrudEnum
from core.manga import MangaSimple
from core.manga_index_type_enum import MangaIndexTypeEnum
from core.chapter import Chapter
from database.crud import chapter_crud
from database import models
from database.crud import user_crud
from database.crud import utils

from database.crud import manga_crud, manga_site_crud
from fastapi import status
from starlette.config import Config


from main import app
from .utils import override_get_db
from database.utils import get_db

from sqlalchemy import update

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

config = Config('.env')


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def db() -> Session:
    db = next(override_get_db())
    utils.delete_all(db)
    manga_site_crud.create_test_manga_site(db)
    return db


@pytest.fixture()
async def client(db) -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://localhost:8000")
    yield client
    print('going to close')
    await client.aclose()


@pytest.fixture()
async def auth_code(client: AsyncClient) -> str:
    response = await client.post("/api/auth/login",
                                 headers={
                                     "X-Requested-With": "application/json"
                                 },
                                 content=config('TEST_AUTH_TOKEN'))

    return response.headers['set-cookie'].split(
        '; ')[0].split('=')[1][1:-1]


@pytest.fixture()
def default_manga(db) -> models.Manga:
    """Helper function to create test manga"""
    name = "Test Manga"
    url = "https://www.test.com"
    return manga_crud.create_manga_with_manga_site_id(db, name, url, 1)


@pytest.fixture()
def mangas(db) -> List[models.Manga]:
    """Helper function to create test mangas"""
    mangas: List[models.Manga] = []
    for i in range(1, 4):
        name = f"Test Manga {i}"
        url = f"https://www.test{i}.com"
        manga = manga_crud.create_manga_with_manga_site_id(db, name, url, 1)
        mangas.append(manga)
    return mangas


class TestUserPublic:
    @pytest.mark.asyncio
    async def test_me_failed(self, client: AsyncClient):
        """Test me without authorization"""
        response = await client.get("/api/user/me")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_favs(self, client: AsyncClient):
        """Test get favorites without authorization"""
        response = await client.get("/api/user/favs")
        assert response.status_code == 403


class TestUserPrivate:
    @pytest.mark.asyncio
    async def test_me_success(self, client: AsyncClient, auth_code: str):
        """Test me with authorization"""
        response = await client.get(
            "/api/user/me", cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_history(self, client: AsyncClient, auth_code: str):
        """Test get history with auth"""
        response = await client.get(
            '/api/user/history', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_add_history_failed(self, client: AsyncClient, auth_code: str):
        """Test add history failed because no manga"""
        response = await client.post(
            '/api/user/add_history/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        assert response.json()['success'] == CrudEnum.Failed

    @pytest.mark.asyncio
    async def test_add_history_successful(self, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test add history successful"""
        response = await client.post(
            '/api/user/add_history/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.get(
            '/api/user/history', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 1
        assert result[0]['name'] == default_manga.name
        assert result[0]['url'] == default_manga.url

    @pytest.mark.asyncio
    async def test_add_history_twice(self, client: AsyncClient, auth_code: str, mangas: List[models.Manga]):
        """Test add history twice"""

        response = await client.post(
            '/api/user/add_history/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.post(
            '/api/user/add_history/2', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.post(
            '/api/user/add_history/3', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.post(
            '/api/user/add_history/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json()['success']

        response = await client.get(
            '/api/user/history', cookies={"Authorization": auth_code})

        result = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 3
        assert result[0]['name'] == mangas[0].name
        assert result[-1]['name'] == mangas[1].name

    @pytest.mark.asyncio
    async def test_del_history_successful(self, db: Session, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test del history successful"""
        user = user_crud.get_users(db)[0]

        success = user_crud.add_history_manga(
            db, default_manga.id, user.id)

        response = await client.delete(
            '/api/user/del_history/1', cookies={"Authorization": auth_code})

        assert success
        assert user.id == 1
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json()['success']
    
    @pytest.mark.asyncio
    async def test_del_history_failed(self, db: Session, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test del history failed"""
        user = user_crud.get_users(db)[0]
        
        response = await client.delete(
            '/api/user/del_history/1', cookies={"Authorization": auth_code})
        
        assert user.id == 1
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        assert response.json()['success'] == CrudEnum.Failed
    
    @pytest.mark.asyncio
    async def test_get_favs(self, client: AsyncClient, auth_code: str):
        """Test get favorites with auth"""
        response = await client.get(
            '/api/user/favs', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert isinstance(result, list)
        assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_add_fav_failed(self, client: AsyncClient, auth_code: str):
        """Test add fav failed"""
        response = await client.post(
            '/api/user/add_fav/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        assert not response.json()['success']

    @pytest.mark.asyncio
    async def test_add_fav_successful(self, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test add fav successful"""        

        response = await client.post(
            '/api/user/add_fav/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.get(
            '/api/user/favs', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 1
        assert result[0]['name'] == default_manga.name
        assert result[0]['url'] == default_manga.url
    
    @pytest.mark.asyncio
    async def test_add_fav_twice_failed(self, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test add fav successful"""

        response = await client.post(
            '/api/user/add_fav/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['success']

        response = await client.post(
            '/api/user/add_fav/1', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        assert not response.json()['success']

        response = await client.get(
            '/api/user/favs', cookies={"Authorization": auth_code})
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert len(result) == 1
        assert result[0]['name'] == default_manga.name
        assert result[0]['url'] == default_manga.url
    
    @pytest.mark.asyncio
    async def test_del_fav_successful(self, db: Session, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test del fav successful"""
        user = user_crud.get_users(db)[0]
        success = user_crud.add_fav_manga(db, default_manga.id, user.id)
        response = await client.delete(
            '/api/user/del_fav/1', cookies={"Authorization": auth_code})

        assert user.id == 1
        assert success
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.json()['success']

    @pytest.mark.asyncio
    async def test_del_fav_failed(self, db: Session, client: AsyncClient, auth_code: str):
        """Test del fav failed"""
        user = user_crud.get_users(db)[0]
        response = await client.delete(
            '/api/user/del_fav/1', cookies={"Authorization": auth_code})

        assert user.id == 1
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
        assert not response.json()['success']

    @pytest.mark.asyncio
    async def test_fav_latest_chapter(self, db: Session, client: AsyncClient, auth_code: str, default_manga: models.Manga):
        """Test fav latest chapter"""
        chapter1 = Chapter(title="Title 1", page_url="https://test1.com")
        chapter2 = Chapter(title="Title 2", page_url="https://test2.com")
        chapter_crud.create_chapter(db, chapter1, default_manga.id, MangaIndexTypeEnum.CHAPTER)
        chapter_crud.create_chapter(db, chapter2, default_manga.id, MangaIndexTypeEnum.CHAPTER)
        
        await client.post(
            f'/api/user/add_fav/{default_manga.id}', cookies={"Authorization": auth_code})

        response = await client.get(
            '/api/user/favs', cookies={"Authorization": auth_code})
        result = response.json()
        manga = MangaSimple(**result[0])
        latest_chap = manga.latest_chapters[MangaIndexTypeEnum.CHAPTER]
        assert latest_chap.title == "Title 2"

