import strawberry
from typing import Optional
from modules.graphql.types import QuestionsG, QuestionTypesG, QuestionSettingsG
from modules.repositories.questions import QuestionsRepository, QuestionTypesRepository, QuestionSettingsRepository
from modules.repositories import FindBy

@strawberry.type
class QuestionsQuery:
    @strawberry.field(graphql_type=list[QuestionsG])
    async def question(self, question_id: int):
        a = await QuestionsRepository().find_one(question_id)
        print(a)
        return a

    # Получение всех вопросов
    @strawberry.field(graphql_type=list[QuestionsG])
    async def questions(self):
        return await QuestionsRepository().find_all()

    # Получение типа вопроса по ID
    @strawberry.field(graphql_type=list[QuestionTypesG])
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
    @strawberry.field(graphql_type=list[QuestionSettingsG])
    async def question_settings(self, question_id: int):
        return await QuestionSettingsRepository().find_by(question_id, FindBy.question_id)