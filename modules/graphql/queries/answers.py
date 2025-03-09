import strawberry
from typing import Optional
from modules.graphql.types import UserAnswersG, VotingRatingsG, VotingAnswersG
from modules.repositories.answers import UserAnswersRepository, VotingRatingsRepository, VotingAnswersRepository

@strawberry.type
class AnswersQuery:
    @strawberry.field(graphql_type=Optional[UserAnswersG])
    async def answer(self, answer_id: int):
        return await UserAnswersRepository().find_one(answer_id)
    
    @strawberry.field(graphql_type=list[UserAnswersG])
    async def answers(self):
        return await UserAnswersRepository().find_all()
    
    @strawberry.field(graphql_type=list[VotingRatingsG])
    async def votings_ratings(self):
        return await VotingRatingsRepository().find_all()

    @strawberry.field(graphql_type=list[VotingRatingsG])
    async def voting_ratings_one_user(self, user_id: int):
        return await VotingRatingsRepository().find_all_by_user_id(user_id)
    
    @strawberry.field(graphql_type=list[VotingRatingsG])
    async def voting_rating_one_question(self, question_id: int):
        return await VotingRatingsRepository().find_all_by_question_id(question_id)
    
    @strawberry.field(graphql_type=list[VotingAnswersG])
    async def votings_answers(self):
        return await VotingAnswersRepository().find_all()
    
    @strawberry.field(graphql_type=Optional[VotingAnswersG])
    async def voting_answer(self, answer_id: int):
        return await VotingAnswersRepository().find_one(answer_id)
    
    @strawberry.field(graphql_type=list[VotingAnswersG])
    async def voting_answer_one_question(self, question_id: int):
        return await VotingAnswersRepository().find_all_by_question_id(question_id)