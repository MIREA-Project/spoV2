import strawberry
from typing import Optional
from modules.graphql.types import QuestionsG, QuestionTypesG
from modules.repositories.questions import QuestionsRepository, QuestionTypesRepository


@strawberry.type
class QuestionsQuery:
    @strawberry.field(graphql_type=Optional[QuestionsG])
    async def question(self, question_id: int):
        return await QuestionsRepository().find_one(question_id)

    # Получение всех вопросов
    @strawberry.field(graphql_type=list[QuestionsG])
    async def questions(self):
        return await QuestionsRepository().find_all()

    # Получение типа вопроса по ID
    @strawberry.field(graphql_type=Optional[QuestionTypesG])
    async def question_type(self, type_id: int):
        return await QuestionTypesRepository().find_one(type_id)

    # Получение всех типов вопросов
    @strawberry.field(graphql_type=list[QuestionTypesG])
    async def question_types(self):
        return await QuestionTypesRepository().find_all()
