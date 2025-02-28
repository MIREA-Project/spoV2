import logging
from contextlib import asynccontextmanager
import strawberry
from strawberry.fastapi import GraphQLRouter

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from db.models import *
from db import init_models
from modules.graphql.context import get_context
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

app.add_middleware(

         CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )
       
        
app.include_router(router)

# add graphql router
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get('/')
async def redirect_to_doc():
    return RedirectResponse(url="/docs")



if __name__ == '__main__':
    uvicorn.run(app, host="192.168.1.167", port=60575)


