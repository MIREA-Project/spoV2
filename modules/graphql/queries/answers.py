import strawberry
from typing import Optional
from modules.graphql.types import UserAnswersG, VotingRatingsG, VotingAnswersG
from modules.repositories.answers import UserAnswersRepository

@strawberry.type
class AnswersQuery:
    @strawberry.field(graphql_type=Optional[UserAnswersG])
    async def answer(self, answer_id: int):
        return await UserAnswersRepository().find_one(answer_id)
    
    @strawberry.field(graphql_type=list[UserAnswersG])
    async def answers(self):
        return await UserAnswersRepository().find_all()
    
    