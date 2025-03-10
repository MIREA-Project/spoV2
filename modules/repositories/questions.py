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