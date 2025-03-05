from db.models import Questions, QuestionTypes
from modules.repositories import SQLAlchemyAbstractRepository


class QuestionsRepository(SQLAlchemyAbstractRepository):
    model = Questions

class QuestionTypesRepository(SQLAlchemyAbstractRepository):
    model = QuestionTypes