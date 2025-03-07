from typing import Optional

from sqlalchemy import select

from db import async_session

from db.models import Questions, QuestionTypes, QuestionSettings
from modules.repositories import SQLAlchemyAbstractRepository


class QuestionsRepository(SQLAlchemyAbstractRepository):
    model = Questions

class QuestionTypesRepository(SQLAlchemyAbstractRepository):
    model = QuestionTypes

class QuestionSettingsRepository(SQLAlchemyAbstractRepository):
    model = QuestionSettings

    async def find_one_by_question_id(self, id_to_find: int) -> Optional[int]:
        async with async_session() as session:
            query = select(self.model).where(self.model.question_id == id_to_find)
            chunked_res = await session.execute(query)
            return chunked_res.fetchone()[0]