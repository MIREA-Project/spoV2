import pytest
from httpx import AsyncClient, ASGITransport

from main import app


class TestUltraBaseTest:
    graphql_model_name = "question"
    graphql_delete_model_name = "delete" + graphql_model_name.capitalize()

    @pytest.mark.asyncio
    async def test_base_query(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={
                "query": """{%s(%sId: 1) {
                                id
                              }  }
            """ % (self.graphql_model_name, self.graphql_model_name)
            })
            assert response.status_code == 200
            assert "data" in response.json()
            assert self.graphql_model_name in response.json()["data"]

    @pytest.mark.asyncio
    async def test_base_delete_mutation(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as client:
            response = await client.post("http://127.0.0.1:8000/graphql", json={"query": """
            mutation {
                %s (%sId: 1) {
                    id
                }  
            }
            """ % (self.graphql_delete_model_name, self.graphql_model_name)})
            assert response.status_code == 200
            assert "data" in response.json()
            assert self.graphql_delete_model_name in response.json()["data"]


class TestQuestion(TestUltraBaseTest):
    graphql_model_name = "question"


class TestAnswer(TestUltraBaseTest):
    graphql_model_name = "answer"
