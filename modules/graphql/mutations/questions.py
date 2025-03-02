import strawberry
from typing import Optional
from modules.graphql.types import QuestionsG
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Мутации (Mutations)
@strawberry.type
class Mutation:
    # Создание нового вопроса
    @strawberry.mutation(graphql_type=QuestionsG)
    async def create_question(
            self,
            user_id: int,
            title: str,
            description: str,
            info: strawberry.types.Info
    ):
        db_session: AsyncSession = info.context.db_session
        new_question_query = insert(Questions).values(
            user_id=user_id,
            title=title,
            description=description,
        ).returning(Questions)
        new_question_chunked = await db_session.execute(new_question_query)
        await db_session.commit()
        return new_question_chunked.scalars().first()

    # Обновление вопроса
    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def update_question(
            self,
            question_id: int,
            info: strawberry.types.Info,
            title: Optional[str] = None,
            description: Optional[str] = None,

    ):
        db_session = info.context.db_session
        # create dict for model
        dict_to_update = {}
        if title:
            dict_to_update['title'] = title
        if description:
            dict_to_update['description'] = description

        query = update(Questions).where(Questions.id == question_id).values(**dict_to_update).returning(Questions)
        result = await db_session.execute(query)
        await db_session.commit()
        return result.scalars().first()

    @strawberry.mutation(graphql_type=Optional[QuestionsG])
    async def delete_question(self, question_id: int, info: strawberry.types.Info) -> bool:
        db_session = info.context.db_session
        try:
            query = delete(Questions).where(Questions.id == question_id)
            await db_session.execute(query)
            await db_session.commit()
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )
        except Exception:
            logging.exception("Failed to delete question")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete question",
            )
