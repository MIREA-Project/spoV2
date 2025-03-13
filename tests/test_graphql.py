import pytest
from httpx import AsyncClient, ASGITransport
from main import app


class TestAnswersQuery:
    @pytest.mark.asyncio
    async def test_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answer(answerId: 1) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_answers_one_user_id(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneUserId(userId: 1) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_answers_one_question_id(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneQuestionId(questionId: 1) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_all_answers(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answers { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_question(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createQuestion(description : "fake description", title: "fake title", userId:1) {
                       createdAt
                        description
                        id
                        title
                        userId
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateAnswer(id: 1, input: {scoreAwarded: 20}) {
                        id
                        questionId
                        userId
                        createdAt
                        scoreAwarded
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteAnswer(id: 1) {
                        id
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_answer_not_found(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answer(answerId: 999) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
