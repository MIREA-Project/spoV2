from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import insert, select, delete, update

from db import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict):
        raise NotImplementedError


class SQLAlchemyAbstractRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> Optional[int]:
        async with async_session() as session:
            query = insert(self.model).values(**data).returning(self.model)
            chunked_res = await session.execute(query)
            await session.commit()
            return chunked_res.fetchone()[0]

    async def find_all(self):
        async with async_session() as session:
            query = select(self.model)
            chunked_res = await session.execute(query)
            return chunked_res.scalars().all()

    async def delete_one(self, id_to_delete: int) -> None:
        async with async_session() as session:
            query = delete(self.model).where(self.model.id == id_to_delete).returning(self.model)
            chunked_res = await session.execute(query)
            await session.commit()
            return chunked_res.all()

    async def find_one(self, id_to_find: int) -> Optional[int]:
        async with async_session() as session:
            query = select(self.model).where(self.model.id == id_to_find)
            chunked_res = await session.execute(query)
            return chunked_res.fetchone()[0]

    async def update_one(self, id_to_update: int, data: dict) -> None:
        async with async_session() as session:
            query = update(self.model).where(self.model.id == id_to_update).values(**data).returning(self.model)
            chunked_res = await session.execute(query)
            await session.commit()
            return chunked_res.fetchone()[0]
