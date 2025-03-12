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
        return await UserAnswersRepository().add_one({
            "question_id": question_id,
            "user_id": user_id,
            "score_awarded": score_awarded
        })
    
    # обновляет ответ пользователя по question_id и user_id
    @strawberry.mutation(graphql_type=Optional[UserAnswersG])
    async def update_user_answer(
        self,
        user_id: int,
        question_id: int,
        score_awarded: Optional[int] = None
    ):
        dict_to_update = {}
        if score_awarded:
            dict_to_update['score_awarded'] = score_awarded
        
        return await UserAnswersRepository().update_one_two_id(user_id, question_id, dict_to_update)
    
    # удаляет все ответы пользователя
    @strawberry.mutation(graphql_type=Optional[UserAnswersG])
    async def delete_user_answers(self, user_id: int):
        try:
            return await UserAnswersRepository().delete_by(user_id, FindBy.user_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # удаляет все ответы на вопрос
    @strawberry.mutation(graphql_type=Optional[UserAnswersG])
    async def delete_question_users_answers(self, question_id: int):
        try:
            return await UserAnswersRepository().delete_by(question_id, FindBy.question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # удаляет все ответы пользователя на определенный вопрос
    @strawberry.mutation(graphql_type=Optional[UserAnswersG])
    async def delete_user_answer(self, user_id: int, question_id: int):
        try:
            return await UserAnswersRepository().delete_one_two_id(user_id, question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # создает рейтинг от пользователя к вопросу
    @strawberry.mutation(graphql_type=VotingRatingsG)
    async def create_voting_rating(self, user_id: int, question_id: int, rating: float):
        return await VotingRatingsRepository().add_one({'user_id': user_id, 'question_id': question_id, 'rating': rating})
    
    # редактирует рейтинг по user_id и question_id
    @strawberry.mutation(graphql_type=Optional[VotingRatingsG])
    async def update_voting_rating(
        self,
        user_id: int,
        question_id: int,
        rating: Optional[float] = None
    ):
        dict_to_update = {}
        if rating:
            dict_to_update['rating'] = rating
        
        return await VotingRatingsRepository().update_one_two_id(user_id, question_id, dict_to_update)
    
    # удаляет все рейтинги от пользователя
    @strawberry.mutation(graphql_type=Optional[VotingRatingsG])
    async def delete_user_ratings(self, user_id: int):
        try:
            return await VotingRatingsRepository().delete_by(user_id, FindBy.user_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # удаляет все рейтинги по вопросу
    @strawberry.mutation(graphql_type=Optional[VotingRatingsG])
    async def delete_question_ratings(self, question_id: int):
        try:
            return await VotingRatingsRepository().delete_by(question_id, FindBy.question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # удаляет рейтинг для определенного вопроса и пользователя
    @strawberry.mutation(graphql_type=Optional[VotingRatingsG])
    async def delete_rating(self, user_id: int, question_id: int):
        try:
            return await VotingRatingsRepository().delete_one_two_id(user_id, question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # создает вариант ответа на вопрос
    @strawberry.mutation(graphql_type=VotingAnswersG)
    async def create_voting_answer(
        self,
        question_id: int,
        title: str,
        description: Optional[str] = None
    ):
        dict_to_add = {
            'question_id': question_id,
            'title': title
        }
        if description:
            dict_to_add['description'] = description
        
        return await VotingAnswersRepository().add_one(dict_to_add)
    
    # редактирует вариант ответа на вопрос по id
    @strawberry.mutation(graphql_type=Optional[VotingAnswersG])
    async def update_voting_answer(
        self,
        voting_answer_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ):
        dict_to_update = {}
        if title:
            dict_to_update['title'] = title
        if description:
            dict_to_update['description'] = description
        
        return await VotingAnswersRepository().update_one(voting_answer_id, dict_to_update)
    
    # удаляем все варианты ответа на вопросы
    @strawberry.mutation(graphql_type=Optional[VotingAnswersG])
    async def delete_voting_answer(self, question_id: int):
        try:
            return await VotingAnswersRepository().delete_by(question_id, FindBy.question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )