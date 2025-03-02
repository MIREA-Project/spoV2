import logging

from fastapi import HTTPException
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.models import *
from sqlalchemy.future import select
from strawberry.fastapi import GraphQLRouter

import strawberry
from typing import Optional

from modules.graphql.context import get_context
import datetime
from decimal import Decimal


# Типы GraphQL
@strawberry.type
class QuestionsG:
    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime


@strawberry.type
class QuestionTypesG:
    id: int
    name: str


@strawberry.type
class QuestionSettingsG:
    question_id: int
    question_type_id: Optional[int]
    expires_at: Optional[datetime.datetime]
    is_anonymous: bool
    is_closed: bool


@strawberry.type
class UserAnswersG:
    id: int
    question_id: int
    user_id: int
    created_at: datetime.datetime
    score_awarded: Optional[int]


@strawberry.type
class VotingRatingsG:
    user_id: int
    question_id: int
    rating: Optional[Decimal]


@strawberry.type
class VotingAnswersG:
    id: int
    question_id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime


# Запросы (Queries)
@strawberry.type
class Query:
    # Получение вопроса по ID
    @strawberry.field(graphql_type=Optional[QuestionsG])
    async def question(self, question_id: int, info: strawberry.types.Info):
        db_session = info.context.db_session
        query = select(Questions).where(Questions.id == question_id)
        result = await db_session.execute(query)
        return result.scalars().one_or_none()

    # Получение всех вопросов
    @strawberry.field(graphql_type=list[QuestionsG])
    async def questions(self, info: strawberry.types.Info):
        db_session = info.context.db_session
        query = select(Questions)
        result = await db_session.execute(query)
        return result.scalars().all()

    # Получение типа вопроса по ID
    @strawberry.field(graphql_type=Optional[QuestionTypesG])
    async def question_type(self, type_id: int, info: strawberry.types.Info):
        db_session = info.context.db_session
        query = select(QuestionTypes).where(QuestionTypes.id == type_id)
        result = await db_session.execute(query)
        return result.scalars().one_or_none()

    # Получение всех типов вопросов
    @strawberry.field(graphql_type=list[QuestionTypesG])
    async def question_types(self, info: strawberry.types.Info):
        db_session = info.context.db_session
        query = select(QuestionTypes)
        result = await db_session.execute(query)
        return result.scalars().all()

    # Добавьте аналогичные методы для других моделей...


# Мутации (Mutations)
@strawberry.type
class Mutation:
    # Создание нового вопроса
    @strawberry.mutation(graphql_type=QuestionsG)
    async def create_question(
            self,
            user_id: int,
            title: str,
            description: str,
            info: strawberry.types.Info
    ):
        db_session: AsyncSession = info.context.db_session
        new_question_query = insert(Questions).values(
            user_id=user_id,
            title=title,
            description=description,
        ).returning(Questions)
        new_question_chunked = await db_session.execute(new_question_query)
        await db_session.commit()
        return new_question_chunked.scalars().first()

    # Обновление вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def update_question(
            self,
            question_id: int,
            info: strawberry.types.Info,
            title: Optional[str] = None,
            description: Optional[str] = None,

    ):
        db_session = info.context.db_session
        # create dict for model
        dict_to_update = {}
        if title:
            dict_to_update['title'] = title
        if description:
            dict_to_update['description'] = description

        query = update(Questions).where(Questions.id == question_id).values(**dict_to_update).returning(Questions)
        result = await db_session.execute(query)
        await db_session.commit()
        return result.scalars().first()

    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def delete_question(self, question_id: int, info: strawberry.types.Info) -> bool:
        db_session = info.context.db_session
        try:
            query = delete(Questions).where(Questions.id == question_id)
            await db_session.execute(query)
            await db_session.commit()
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )


#     # Добавьте аналогичные методы для других моделей...


# add graphql router
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
