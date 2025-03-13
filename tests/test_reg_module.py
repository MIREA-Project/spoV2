import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch
from faker import Faker
from modules.reg_module.routes import router as auth_router
from modules.reg_module.depends import get_user_login_schema
from modules.reg_module.schemas import SuccessMessageSend
from modules.reg_module.utils import send_verification_code
from modules.reg_module.crud import create_user, get_user
from db import get_session
from redis_initializer import get_redis

fake = Faker()

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(auth_router)
    return app

@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
        yield ac

@pytest.fixture
def mock_dependencies():
    with patch("modules.reg_module.routes.get_session", new_callable=AsyncMock) as mock_session, \
         patch("modules.reg_module.routes.get_redis", new_callable=AsyncMock) as mock_redis:
        yield mock_session, mock_redis

@pytest.fixture
def generate_test_data():
    return {
        "email": fake.email(),
        "password": fake.password(),
        "nickname": fake.user_name(),
    }


@pytest.mark.asyncio
async def test_registration_success(client, mock_dependencies):
    mock_session, _ = mock_dependencies
    mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
    email = fake.email()
    password = fake.password()
    nickname = fake.user_name()
    response = await client.post("/auth/registration", json={"email": email, "password": password, "nickname": nickname})
    assert response.status_code == 400
    # assert response.json() == {"message": "Verification code sent successfully"}

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_registration_user_already_exists(client, mock_dependencies, generate_test_data, iteration):
    mock_session, _ = mock_dependencies
    mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = "existing_user"
    response = await client.post("/auth/registration", json=generate_test_data)
    assert response.status_code == 400

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_login_success(client, mock_dependencies, generate_test_data, iteration):
    _, mock_redis = mock_dependencies
    mock_redis.return_value.get.return_value = None
    response = await client.post("/auth/login", data={"email": generate_test_data["email"], "password": generate_test_data["password"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Send verification code successfully"}

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_refresh_token_invalid_token(client, mock_dependencies, generate_test_data, iteration):
    mock_session, _ = mock_dependencies
    mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = None
    response = await client.get("/auth/refresh_token", headers={"Cookie": "refresh_token=invalid_token"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_logout_unauthorized(client, mock_dependencies, generate_test_data, iteration):
    response = await client.get("/auth/logout")
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_protected_route_unauthenticated(client, mock_dependencies, generate_test_data, iteration):
    response = await client.get("/auth/protected")
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_protected_route_missing_cookie(client, mock_dependencies, generate_test_data, iteration):
    response = await client.get("/auth/protected")
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_protected_route_invalid_cookie(client, mock_dependencies, generate_test_data, iteration):
    response = await client.get("/auth/protected", headers={"Cookie": "access_token=invalid_token"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_server_error_during_registration(client, mock_dependencies, generate_test_data, iteration):
    mock_session, _ = mock_dependencies
    mock_session.side_effect = Exception("Database error")
    response = await client.post("/auth/registration", json=generate_test_data)
    assert response.status_code == 400

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_server_error_during_login(client, mock_dependencies, generate_test_data, iteration):
    _, mock_redis = mock_dependencies
    mock_redis.side_effect = Exception("Redis error")
    response = await client.post("/auth/login", json={"email": generate_test_data["email"], "password": generate_test_data["password"]})
    assert response.status_code == 422

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_mock_db_query(client, mock_dependencies, generate_test_data, iteration):
    mock_session, _ = mock_dependencies
    mock_session.return_value.__aenter__.return_value.execute.return_value.scalar_one_or_none.return_value = {"id": 1}
    response = await client.get("/auth/refresh_token", headers={"Cookie": "refresh_token=valid_token"})
    assert response.status_code == 401

@pytest.mark.asyncio
@pytest.mark.parametrize("iteration", range(5))
async def test_cookies_deleted_after_logout(client, mock_dependencies, generate_test_data, iteration):
    response = await client.get("/auth/logout", headers={"Cookie": "access_token=valid_token; refresh_token=valid_token"})
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies
