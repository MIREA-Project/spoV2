import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from db import init_models
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


@app.get('/')
async def redirect_to_doc():
    return RedirectResponse(url="/docs")


if __name__ == '__main__':
    uvicorn.run(app)
