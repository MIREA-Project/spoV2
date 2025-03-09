from db.models import UserAnswers
from modules.repositories import SQLAlchemyAbstractRepository


class UserAnswersRepository(SQLAlchemyAbstractRepository):
    model = UserAnswers