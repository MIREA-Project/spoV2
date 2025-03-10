import strawberry

import logging
from typing import Optional
from fastapi import HTTPException, status
from modules.graphql.types import QuestionsG, QuestionTypesG

from modules.repositories.questions import QuestionsRepository, QuestionTypesRepository


# Мутации (Mutations)
@strawberry.type
class QuestionsMutation:
    # Создание нового вопроса
    @strawberry.mutation(graphql_type=QuestionsG)
    async def create_question(
            self,
            user_id: int,
            title: str,
            description: str,
    ):
        return await QuestionsRepository().add_one({"user_id": user_id, "title": title, "description": description})

    # Обновление вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def update_question(
            self,
            question_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,

    ):
        # create dict for model
        dict_to_update = {}
        if title:
            dict_to_update['title'] = title
        if description:
            dict_to_update['description'] = description

        return await QuestionsRepository().update_one(question_id, dict_to_update)

    # Удаление вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def delete_question(self, question_id: int) -> bool:
        try:
            return await QuestionsRepository().delete_one(question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
    
    # Создание нового типа вопроса
    @strawberry.mutation(graphql_type=QuestionTypesG)
    async def create_question_type(self, name: str):
        return await QuestionTypesRepository().add_one({"name": name})
    
    # Обновлние типа вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionTypesG])
    async def update_question_type(self, type_id: int, name: str):
        dict_to_update = {}
        if name:
            dict_to_update['name'] = name
        
        return await QuestionTypesRepository().update_one(type_id, dict_to_update)
    
    # удаление типа вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionTypesG])
    async def delete_question_type(self, type_id: int):
        try:
            return await QuestionTypesRepository().delete_one(type_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
