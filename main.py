import logging
from contextlib import asynccontextmanager
from db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext
import strawberry
from strawberry.fastapi import GraphQLRouter

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from db.models import *
from db import init_models
from modules.graphql.example import Query
from redis_initializer import init_redis, close_redis
from modules.reg_module.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await init_redis()
    await init_models()
    yield
    await close_redis()


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "displayRequestDuration": True,  # Показать длительность запросов
    }
)
app.include_router(router)
# Монтируем GraphQL роутер в FastAPI
# Создаем схему GraphQL
# Контекст для GraphQL
class GraphqlContext(BaseContext):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


# Функция для создания контекста
async def get_context(db_session: AsyncSession = Depends(get_session)) -> GraphqlContext:
    return GraphqlContext(db_session=db_session)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get('/')
async def redirect_to_doc():
    return RedirectResponse(url="/docs")


if __name__ == '__main__':
    uvicorn.run(app)
