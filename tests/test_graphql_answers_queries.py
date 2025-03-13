import pytest
from httpx import AsyncClient, ASGITransport
from main import app

class TestQuestionsQueries:
    @pytest.mark.asyncio
    async def test_question(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ question(questionId: 1) { id userId title description } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_questions(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ questions { id userId title description } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_question_type(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ questionType(typeId: 1) { id name } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_question_types(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ questionTypes { id name } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_questions_settings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ questionsSettings { id questionId questionTypeId isAnonymous isClosed } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_question_settings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ questionSettings(questionId: 1) { id questionId questionTypeId isAnonymous isClosed } }"
            })
            assert response.status_code == 200
