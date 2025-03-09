import strawberry
from typing import Optional
from modules.graphql.types import UserInfoG
from modules.repositories.users import UsersInfoRepository


@strawberry.type
class UserInfoQuery:
    @strawberry.field(graphql_type=Optional[UserInfoG])
    async def user(self, user_id: int):
        return await UsersInfoRepository().find_one(user_id)
    
    @strawberry.field(graphql_type=list[UserInfoG])
    async def users(self):
        return await UsersInfoRepository().find_all()