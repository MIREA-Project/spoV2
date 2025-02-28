from typing import Optional
import logging
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from modules.reg_module.utils import get_password_hash
from . import schemas


async def get_user(
        email: str,
        session: AsyncSession
) -> Optional[models.User]:
    query = select(models.User).where(models.User.email == email)
    chunked_result = await session.execute(query)
    return chunked_result.scalars().one_or_none()


async def create_user(
        user_info: schemas.UserRegisterInfo,
        session: AsyncSession
) -> models.User | None:
    try:
            user_info.password = get_password_hash(user_info.password)
            user_info_dict = user_info.model_dump()
            new_user_model = models.User(**user_info_dict)
            session.add(new_user_model)
            await session.commit()
            return new_user_model
    except Exception:
        logging.exception("Failed to create user")
        return False
