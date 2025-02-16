from contextlib import asynccontextmanager
import hmac
import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from redis.asyncio import Redis

from depends import get_form_data, validate_code
import schemas
from utils import send_verification_code
from redis_utils import init_redis, close_redis, get_redis
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await init_redis()
    yield
    await close_redis()


app = FastAPI(
    lifespan=lifespan
)


@app.post('/auth')
async def auth_user(
        phone_number: schemas.PhoneNumber = Depends(get_form_data),
        redis_client: Redis = Depends(get_redis)
) -> schemas.SuccessMessageSend:
    try:
        await send_verification_code(phone_number.phone_number, redis_client)
        return schemas.SuccessMessageSend(
            message="Verification code sent successfully",
        )
    except Exception as e:
        logging.exception("Exception")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.get("/verify_code")
async def verify_code(
        user_auth_info: schemas.UserAuthInfo = Depends(validate_code),
        redis_client: Redis = Depends(get_redis)
):
    backend_code_from_user = await redis_client.get(
        user_auth_info.phone_number.phone_number
    )
    if backend_code_from_user is None:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Code lifetime is expired"
        )
    # using to avoid time attack
    if hmac.compare_digest(backend_code_from_user, str(user_auth_info.code)):
        # delete code from redis
        await redis_client.delete(user_auth_info.phone_number.phone_number)
        # user auth success!
        # set jwt
        return {"message": "auth sucess"}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Wrong code'
    )


if __name__ == '__main__':
    uvicorn.run(app)
