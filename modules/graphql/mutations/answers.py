import strawberry

import logging
from typing import Optional
from fastapi import HTTPException, status
from modules.graphql.types import UserAnswersG, VotingRatingsG, VotingAnswersG
from modules.repositories.answers import UserAnswersRepository, VotingAnswersRepository, VotingRatingsRepository
from modules.repositories import FindBy

@strawberry.type
class AnswersMutation:

    # создание user_answers
    @strawberry.mutation(graphql_type=UserAnswersG)
    async def create_user_answer(
        self,
        question_id: int,
        user_id: int,
        score_awarded: int
    ):
        return await UserAnswersRepository.add_one({
            "question_id": question_id,
            "user_id": user_id,
            "score_awarded": score_awarded
        })