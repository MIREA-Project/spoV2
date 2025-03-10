from typing import Optional

from sqlalchemy import select

from db import async_session

from db.models import UserAnswers, VotingRatings, VotingAnswers
from modules.repositories import SQLAlchemyAbstractRepository


class UserAnswersRepository(SQLAlchemyAbstractRepository):
    model = UserAnswers
        

class VotingRatingsRepository(SQLAlchemyAbstractRepository):
    model = VotingRatings


class VotingAnswersRepository(SQLAlchemyAbstractRepository):
    model = VotingAnswers
