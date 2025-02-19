import hmac
import logging
import random

from fastapi import Depends, status, HTTPException, Response, APIRouter
from redis.asyncio import Redis

from . import schemas
from .depends import get_form_data, validate_code
from redis_initializer import get_redis
from .jwt_module import jwt_schemas
from .jwt_module.creator import create_access_token, create_refresh_token
from .jwt_module.depends import get_user_from_token, get_user_id_from_refresh_token
from .utils import send_verification_code

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

database: dict[int, schemas.User] = {}


@router.post('/auth')
async def auth_user(
        phone_number: schemas.PhoneNumber = Depends(get_form_data),
        redis_client: Redis = Depends(get_redis)
) -> schemas.SuccessMessageSend:
    try:
        await send_verification_code(phone_number.phone_number, redis_client)
        return schemas.SuccessMessageSend(
            message="Verification code sent successfully",
        )
    except Exception:
        logging.exception("Exception")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/verify_code")
async def verify_code(
        response: Response,
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
        # insert or get user from db\
        user = schemas.User(
            id=random.randint(0, 10 ** 6),
            phone_number=user_auth_info.phone_number,
        )
        database[user.id] = user

        # user auth success!
        access_token: str = create_access_token(user=user)
        refresh_token: str = create_refresh_token(user.id)

        # set jwt
        response.set_cookie(
            key=jwt_schemas.TokenType.access_token.value,
            value=access_token,
            httponly=True,
            secure=False,  # MAKE TRUE ON PRODUCTION
        )
        response.set_cookie(
            key=jwt_schemas.TokenType.refresh_token.value,
            value=refresh_token,
            httponly=True,
            secure=False,  # MAKE TRUE ON PRODUCTION
        )
        return {"message": "auth success"}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Wrong code'
    )


@router.get("/refresh_token")
async def get_new_access_token(
        response: Response,
        user_id: int = Depends(get_user_id_from_refresh_token),
):
    # get user from database
    user = database[user_id]

    # set jwt
    access_token = create_access_token(user=user)

    response.set_cookie(
        key=jwt_schemas.TokenType.access_token.value,
        value=access_token,
        httponly=True,
        secure=False,  # MAKE TRUE ON PRODUCTION
    )


@router.get("/logout")
async def logout(
        response: Response,
        _=Depends(get_user_from_token)
):
    response.delete_cookie(
        key=jwt_schemas.TokenType.access_token.value,
    )
    response.delete_cookie(
        key=jwt_schemas.TokenType.refresh_token.value,
    )


@router.get("/protected")
async def start_page(
        _=Depends(get_user_from_token)
):
    return {"status": "success"}
