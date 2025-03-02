import strawberry
from typing import Optional
from modules.graphql.types import QuestionsG, QuestionTypesG
from sqlalchemy import select
from db.models import Questions, QuestionTypes


@strawberry.type
class QuestionsQuery:
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
