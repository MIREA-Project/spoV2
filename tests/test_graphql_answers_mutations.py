import pytest
from httpx import AsyncClient, ASGITransport
from main import app

class TestAnswersMutations:
    @pytest.mark.asyncio
    async def test_create_user_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createUserAnswer(questionId: 1, userId: 1, scoreAwarded: 5) {
                        id
                        questionId
                        userId
                        scoreAwarded
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_user_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateUserAnswer(userId: 1, questionId: 1, scoreAwarded: 10) {
                        id
                        questionId
                        userId
                        scoreAwarded
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_user_answers(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteUserAnswers(userId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_question_users_answers(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteQuestionUsersAnswers(questionId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_user_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteUserAnswer(userId: 1, questionId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_voting_rating(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createVotingRating(userId: 1, questionId: 1, rating: 4.5) {
                        id
                        userId
                        questionId
                        rating
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_voting_rating(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateVotingRating(userId: 1, questionId: 1, rating: 5.0) {
                        id
                        userId
                        questionId
                        rating
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_user_ratings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteUserRatings(userId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_question_ratings(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteQuestionRatings(questionId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_rating(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteRating(userId: 1, questionId: 1)
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_voting_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    createVotingAnswer(questionId: 1, title: "Test Answer", description: "Test Description") {
                        id
                        questionId
                        title
                        description
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_update_voting_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    updateVotingAnswer(votingAnswerId: 1, title: "Updated Title", description: "Updated Description") {
                        id
                        title
                        description
                    }
                }
                """
            })
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_voting_answer(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """
                mutation {
                    deleteVotingAnswer(questionId: 1)
                }
                """
            })
            assert response.status_code == 200
