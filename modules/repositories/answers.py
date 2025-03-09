from typing import Optional

from sqlalchemy import select

from db import async_session

from db.models import UserAnswers, VotingRatings, VotingAnswers
from modules.repositories import SQLAlchemyAbstractRepository


class UserAnswersRepository(SQLAlchemyAbstractRepository):
    model = UserAnswers

class VotingRatingsRepository(SQLAlchemyAbstractRepository):
    model = VotingRatings

    async def find_all_by_user_id(self, id_to_find: int) -> Optional[int]:
        async with async_session() as session:
            query = select(self.model).where(self.model.user_id == id_to_find)
            chunked_res = await session.execute(query)
            return chunked_res.scalars().all()

    async def find_all_by_question_id(self, id_to_find: int) -> Optional[int]:
        async with async_session() as session:
            query = select(self.model).where(self.model.question_id == id_to_find)
            chunked_res = await session.execute(query)
            return chunked_res.scalars().all()

class VotingAnswersRepository(SQLAlchemyAbstractRepository):
    model = VotingAnswers

    async def find_all_by_question_id(self, id_to_find: int) -> Optional[int]:
        async with async_session() as session:
            query = select(self.model).where(self.model.question_id == id_to_find)
            chunked_res = await session.execute(query)
            return chunked_res.scalars().all()