import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_questions():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        response = await client.post("http://127.0.0.1:8000/graphql", json=
        {
            "query": "{\n  questions {    title    userId    id    description  }}"})
        assert response.status_code == 200
