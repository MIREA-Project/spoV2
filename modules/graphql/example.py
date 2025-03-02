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
    creator_id: int
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
    type_id: Optional[int]
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
class VotingOptionsG:
    id: int
    question_id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime


@strawberry.type
class NumericAnswersG:
    option_id: int
    value: Decimal


@strawberry.type
class TextAnswersG:
    option_id: int
    value: str


@strawberry.type
class BooleanAnswersG:
    option_id: int
    value: bool


# Запросы (Queries)
@strawberry.type
class Query:
    # Получение вопроса по ID
    @strawberry.field
    async def question(self, question_id: int, info: strawberry.types.Info) -> Optional[QuestionType]:
        db_session = info.context.db_session
        query = select(Questions).where(Questions.id == question_id)
        result = await db_session.execute(query)
        question_model = result.scalars().one_or_none()
        if question_model:
            return QuestionsG(
                id=question_model.id,
                creator_id=question_model.creator_id,
                title=question_model.title,
                description=question_model.description,
                created_at=question_model.created_at
            )
        return None

    # Получение всех вопросов
    @strawberry.field
    async def questions(self, info: strawberry.types.Info) -> list[QuestionType]:
        db_session = info.context.db_session
        query = select(Questions)
        result = await db_session.execute(query)
        question_models = result.scalars().all()
        return [
            QuestionType(
                id=q.id,
                creator_id=q.creator_id,
                title=q.title,
                description=q.description,
                created_at=q.created_at
            ) for q in question_models
        ]

    # Получение типа вопроса по ID
    @strawberry.field
    async def question_type(self, type_id: int, info: strawberry.types.Info) -> Optional[QuestionTypeType]:
        db_session = info.context.db_session
        query = select(QuestionTypes).where(QuestionTypes.id == type_id)
        result = await db_session.execute(query)
        type_model = result.scalars().first()
        if type_model:
            return QuestionTypeType(id=type_model.id, name=type_model.name)
        return None

    # Получение всех типов вопросов
    @strawberry.field
    async def question_types(self, info: strawberry.types.Info) -> list[QuestionTypeType]:
        db_session = info.context.db_session
        query = select(QuestionTypes)
        result = await db_session.execute(query)
        type_models = result.scalars().all()
        return [QuestionTypeType(id=t.id, name=t.name) for t in type_models]

    # Добавьте аналогичные методы для других моделей...


# Мутации (Mutations)
@strawberry.type
class Mutation:
    # Создание нового вопроса
    @strawberry.mutation
    async def create_question(self, creator_id: int, title: str, description: Optional[str],
                              info: strawberry.types.Info) -> QuestionType:
        db_session = info.context.db_session
        new_question = Questions(creator_id=creator_id, title=title, description=description)
        db_session.add(new_question)
        await db_session.commit()
        await db_session.refresh(new_question)
        return QuestionType(
            id=new_question.id,
            creator_id=new_question.creator_id,
            title=new_question.title,
            description=new_question.description,
            created_at=new_question.created_at
        )

    # Обновление вопроса
    @strawberry.mutation
    async def update_question(self, question_id: int, title: str, description: Optional[str],
                              info: strawberry.types.Info) -> Optional[QuestionType]:
        db_session = info.context.db_session
        query = select(Questions).where(Questions.id == question_id)
        result = await db_session.execute(query)
        question_model = result.scalars().first()
        if question_model:
            question_model.title = title
            question_model.description = description
            await db_session.commit()
            await db_session.refresh(question_model)
            return QuestionType(
                id=question_model.id,
                creator_id=question_model.creator_id,
                title=question_model.title,
                description=question_model.description,
                created_at=question_model.created_at
            )
        return None

    # Удаление вопроса
    @strawberry.mutation
    async def delete_question(self, question_id: int, info: strawberry.types.Info) -> bool:
        db_session = info.context.db_session
        query = select(Questions).where(Questions.id == question_id)
        result = await db_session.execute(query)
        question_model = result.scalars().first()
        if question_model:
            await db_session.delete(question_model)
            await db_session.commit()
            return True
        return False

    # Добавьте аналогичные методы для других моделей...


# add graphql router
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
