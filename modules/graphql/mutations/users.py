import strawberry

import logging
from typing import Optional
from fastapi import HTTPException, status
from modules.graphql.types import UserInfoG

from modules.repositories.users import UsersInfoRepository


@strawberry.type
class UsersMutation:
    
    # Создание нового юзера
    @strawberry.mutation(graphql_type=UserInfoG)
    async def create_user(
        self,
        nickname: str,
        email: str
    ):
        return await UsersInfoRepository().add_one({
            "nickname": nickname,
            "email": email,
            "correct_vote_count": 0,
            "score": 0
            })
    
    # Обновление юзера
    @strawberry.mutation(graphql_type=Optional[UserInfoG])
    async def update_user(
        self,
        user_id: int,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        correct_vote_count: Optional[int] = None,
        score: Optional[int] = None
    ):
        dict_to_update = {}
        if nickname:
            dict_to_update['nickname'] = nickname
        if email:
            dict_to_update['email'] = email
        if correct_vote_count:
            dict_to_update['correct_vote_count'] = correct_vote_count
        if score:
            dict_to_update['score'] = score
        
        return await UsersInfoRepository().update_one(user_id, dict_to_update)
    
    # Удаление юзера
    @strawberry.mutation(graphql_type=Optional[UserInfoG])
    async def delete_user(self, user_id: int):
        try:
            return await UsersInfoRepository().delete_one(user_id)
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )