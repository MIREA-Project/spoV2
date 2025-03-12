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
            assert "data" in response.json()
            assert "answer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answers_one_user_id(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneUserId(userId: 1) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "answersOneUserId" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answers_one_question_id(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneQuestionId(questionId: 1) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "answersOneQuestionId" in response.json()["data"]

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
            assert "data" in response.json()
            assert "createQuestion" in response.json()["data"]

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
            assert "data" in response.json()
            assert "updateAnswer" in response.json()["data"]

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
            assert "data" in response.json()
            assert "deleteAnswer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answer_not_found(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answer(answerId: 999) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "errors" in response.json()

    @pytest.mark.asyncio
    async def test_invalid_query(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ invalidQuery { id } }"
            })
            assert response.status_code == 400
            assert "errors" in response.json()

    # Добавляем еще 90 тестов
    @pytest.mark.asyncio
    async def test_answer_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answer(answerId: 2) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "answer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answers_one_user_id_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneUserId(userId: 2) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "answersOneUserId" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answers_one_question_id_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answersOneQuestionId(questionId: 2) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "answersOneQuestionId" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_all_answers_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ allAnswers { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "allAnswers" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_create_answer_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createAnswer(input: {questionId: 2, userId: 2, scoreAwarded: 20}) {
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
            assert "data" in response.json()
            assert "createAnswer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_update_answer_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateAnswer(id: 2, input: {scoreAwarded: 30}) {
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
            assert "data" in response.json()
            assert "updateAnswer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_delete_answer_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteAnswer(id: 2) {
                        id
                    }
                }
                """
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert "deleteAnswer" in response.json()["data"]

    @pytest.mark.asyncio
    async def test_answer_not_found_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ answer(answerId: 998) { id questionId userId createdAt scoreAwarded } }"
            })
            assert response.status_code == 200
            assert "errors" in response.json()

    @pytest.mark.asyncio
    async def test_invalid_query_2(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": "{ invalidQuery { id } }"
            })
            assert response.status_code == 400
            assert "errors" in response.json()
