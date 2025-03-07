import strawberry
from typing import Optional
from modules.graphql.types import QuestionsG, QuestionTypesG, QuestionSettingsG
from modules.repositories.questions import QuestionsRepository, QuestionTypesRepository, QuestionSettingsRepository


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

    # получение всех настроек всех вопросов
    @strawberry.field(graphql_type=list[QuestionSettingsG])
    async def questions_settings(self):
        return await QuestionSettingsRepository().find_all()

    # получение настроек одного вопроса
    @strawberry.field(graphql_type=Optional[QuestionSettingsG])
    async def question_settings(self, question_id: int):
        return await QuestionSettingsRepository().find_one_by_question_id(question_id)