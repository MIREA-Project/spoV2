import pytest
from httpx import AsyncClient, ASGITransport
from main import app


class TestQuestionsMutations:
    @pytest.mark.asyncio
    async def test_create_question(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createQuestion(userId: 1, title: "Test Title", description: "Test Description") {
                        id
                        userId
                        title
                        description
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_question(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateQuestion(questionId: 1, title: "Updated Title") {
                        id
                        title
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_question(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteQuestion(questionId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_question_type(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createQuestionType(name: "Test Type") {
                        id
                        name
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_question_type(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateQuestionType(typeId: 1, name: "Updated Type") {
                        id
                        name
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_question_type(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteQuestionType(typeId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_question_settings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createQuestionSettings(
                        questionId: 1,
                        questionTypeId: 1,
                        isAnonymous: true,
                        isClosed: false
                    ) {
                        id
                        questionId
                        questionTypeId
                        isAnonymous
                        isClosed
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_question_settings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateQuestionSettings(
                        questionId: 1,
                        questionTypeId: 2,
                        isAnonymous: false,
                        isClosed: true
                    ) {
                        id
                        questionId
                        questionTypeId
                        isAnonymous
                        isClosed
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_question_settings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteQuestionSettings(questionId: 1)
                }
                """
            })
            assert response.status_code == 200
