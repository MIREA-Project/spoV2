import strawberry
from sqlalchemy.future import select

from db.models import User


# Тип данных для GraphQL
@strawberry.type
class GraphUser:
    id: int
    nickname: str
    email: str
    correct_vote_count: int
    score: int


# Запросы (Queries) для GraphQL
@strawberry.type
class Query:
    @strawberry.field
    async def user(self,
                   user_id: int,
                   info: strawberry.types.Info
                   ) -> GraphUser | None:
        session = info.context.db_session
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user_model = result.scalars().first()
        if user_model:
            return GraphUser(
                id=user_model.id,
                nickname=user_model.nickname,
                email=user_model.email,
                correct_vote_count=user_model.correct_vote_count,
                score=user_model.score
            )
        return None
