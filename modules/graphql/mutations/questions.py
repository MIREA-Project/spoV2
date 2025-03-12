import strawberry

import logging
from typing import Optional
from fastapi import HTTPException, status
from modules.graphql.types import QuestionsG, QuestionTypesG, QuestionSettingsG

from modules.repositories.questions import QuestionsRepository, QuestionTypesRepository, QuestionSettingsRepository
from modules.repositories import FindBy


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
    async def update_question_type(self, type_id: int, name: Optional[str] = None):
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

    # Создание новых настроек вопроса 
    @strawberry.mutation(graphql_type=QuestionSettingsG)
    async def create_question_settings(
            self,
            question_id: int,
            question_type_id: int,
            is_anonymous: bool,
            is_closed: bool
    ):

        return await QuestionSettingsRepository().add_one({
            "question_id": question_id,
            "question_type_id": question_type_id,
            "is_anonymous": is_anonymous,
            "is_closed": is_closed
        })

    # Обновление настроек вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionSettingsG])
    async def update_question_settings(
            self,
            question_id: int,
            question_type_id: Optional[int] = None,
            is_anonymous: Optional[bool] = None,
            is_closed: Optional[bool] = None
    ):
        dict_to_update = {}
        if question_type_id:
            dict_to_update['question_type_id'] = question_type_id
        if is_anonymous:
            dict_to_update['is_anonymous'] = is_anonymous
        if is_closed:
            dict_to_update['is_closed'] = is_closed

        return await QuestionSettingsRepository().update_by(question_id, dict_to_update, FindBy.question_id)

    # Удаление настроек вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionSettingsG])
    async def delete_question_settings(self, question_id: int):
        try:
            return await QuestionSettingsRepository().delete_by(question_id, FindBy.question_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
