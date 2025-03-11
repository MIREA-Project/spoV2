import pytest
import asyncio
from httpx import AsyncClient

from main import app
from db import Base, get_session
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    async with get_session() as session:
        yield session

@pytest.fixture(scope="function")
async def client(db_session):
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac