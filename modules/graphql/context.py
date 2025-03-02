from modules.reg_module import schemas

from db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from modules.reg_module.jwt_module.depends import get_user_from_token


class GraphqlContext(BaseContext):
    def __init__(self, db_session: AsyncSession, user: schemas.User = None):
        """
        create context from fastapi for graphql
        """
        self.db_session = db_session
        # self.user = user


# Функция для создания контекста
async def get_context(
        db_session: AsyncSession = Depends(get_session),
        # user_schema: schemas.User = Depends(get_user_from_token)
) -> GraphqlContext:
    return GraphqlContext(db_session=db_session)
