import pytest
from httpx import AsyncClient, ASGITransport
from main import app

class TestUsersMutations:
    @pytest.mark.asyncio
    async def test_create_user(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createUser(nickname: "testuser", email: "test@example.com") {
                        id
                        nickname
                        email
                        correctVoteCount
                        score
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_user(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateUser(userId: 1, nickname: "updateduser", email: "updated@example.com", correctVoteCount: 5, score: 100) {
                        id
                        nickname
                        email
                        correctVoteCount
                        score
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_user(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteUser(userId: 1)
                }
                """
            })
            assert response.status_code == 200
    
    