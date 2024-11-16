import pytest
import json

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *

from httpx import ASGITransport, AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager( session_factory=async_session_maker_null_pool ) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db

app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_test_data_in_db(setup_database):
    with open('tests/mock_hotels.json', 'r', encoding='utf-8') as file:
        hotels_data = json.load(file)
        # print(f'{hotels_data=}')

    with open('tests/mock_rooms.json', 'r', encoding='utf-8') as file:
        rooms_data = json.load(file)
        # print(f'{rooms_data=}')

    async with DBManager( session_factory=async_session_maker_null_pool ) as db_:
        await db_.hotels.add_bulk([HotelAdd(**hotel) for hotel in hotels_data])
        await db_.rooms.add_bulk([RoomAdd(**room) for room in rooms_data])
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient( transport=ASGITransport( app=app ), base_url="http://test" ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234",
            }
        )



