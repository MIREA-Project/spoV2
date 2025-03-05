import pytest
from httpx import AsyncClient, ASGITransport

from main import app

@pytest.mark.asyncio
async def test_questions():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        response = await client.get("/docs")
        print(response)
