from database.crud import chapter_crud
from core.utils import get_manga_site_common
from database.crud import manga_site_crud
from database.crud import utils
from database.crud import manga_crud
from database.utils import get_db
from .utils import override_get_db, override_get_manga_site_common
from main import app
from starlette.config import Config
import json

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
config = Config('.env')

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_manga_site_common] = override_get_manga_site_common


@pytest.fixture(scope='module')
def db() -> Session:
    db = next(override_get_db())
    utils.delete_all(db)
    manga_site_crud.create_test_manga_site(db)
    return db


@pytest.fixture(scope='module')
async def client(db) -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://localhost:8000")
    yield client
    print('going to close')
    await client.aclose()


class TestMain():

    @pytest.mark.asyncio
    async def test_search_manga(self, db: Session, client: AsyncClient):
        """Test search manga on MHR"""
        response = await client.get("/api/search/manhuaren/火影")
        results = response.json()
        assert response.status_code == 200
        for manga in results:
            assert manga['id'] is not None
            if manga['name'] == '火影忍者':
                url = manga['url']
                assert url == 'https://www.manhuaren.com/manhua-huoyingrenzhe-naruto/'

                db_manga = manga_crud.get_manga_by_url(db, url)

                assert db_manga is not None
                assert db_manga.name == manga['name']

    @pytest.mark.asyncio
    async def test_get_index(self, client: AsyncClient):
        """Test get index on MHR"""
        await client.get("/api/search/manhuaren/火影")
        response = await client.get(
            "/api/index/manhuaren/1")
        result = response.json()
        assert response.status_code == 200
        assert result['name'] == '火影忍者'
        assert result['finished'] == True
        assert result['id'] is not None

    @pytest.mark.asyncio
    async def test_get_chapter(self, db: Session, client: AsyncClient):
        """Test get chapter on MHR"""
        page_url = "https://www.manhuaren.com/m424056/"

        response = await client.get("/api/search/manhuaren/海盜")
        manga_id = None
        for manga in response.json():
            if 'manhua-haidaozhanji' in manga['url']:
                manga_id = manga['id']
        assert manga_id is not None

        await client.get(f'/api/index/manhuaren/{manga_id}')

        response = await client.get(
            f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
        assert response.status_code == 200

        content = response.content.decode()
        results = [json.loads(item_str[6:])
                   for item_str in content.split('\n\n')[:-2]]
        assert len(results) == 8
        for item in results:
            assert "idx" in item
            assert "total" in item
            assert "pic_path" in item

        db_pages = chapter_crud.get_chapter_pages(db, page_url)
        assert len(db_pages) == 8

    @pytest.mark.asyncio
    async def test_get_chapter_twice(self, client: AsyncClient):
        """Test get chapter twice on MHR get same result"""
        page_url = "https://www.manhuaren.com/m424056/"
        response = await client.get("/api/search/manhuaren/海盜")
        manga_id = None
        for manga in response.json():
            if 'manhua-haidaozhanji' in manga['url']:
                manga_id = manga['id']
        assert manga_id is not None

        await client.get(f'/api/index/manhuaren/{manga_id}')
        response = await client.get(
            f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
        response2 = await client.get(
            f'/api/chapter/manhuaren/{manga_id}', params={'page_url': page_url})
        assert response.status_code == 200

        content = response.content.decode()
        results = [json.loads(item_str[6:])
                   for item_str in content.split('\n\n')[:-2]]

        content2 = response2.content.decode()
        results2 = [json.loads(item_str[6:])
                    for item_str in content2.split('\n\n')[:-2]]
        print(results)

        result_dict = {item['idx']: item for item in results}
        for item in results2:
            assert result_dict[item['idx']] == item
