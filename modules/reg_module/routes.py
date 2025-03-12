import hmac
import logging

from fastapi import Depends, status, HTTPException, Response, APIRouter
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session, models
from redis_initializer import get_redis
from . import schemas
from .depends import get_user_login_schema
from .jwt_module import jwt_schemas
from .jwt_module.creator import create_access_token, create_refresh_token
from .jwt_module.depends import get_user_from_token, get_user_id_from_refresh_token
from .utils import send_verification_code
from . import crud as db

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/registration")
async def add_new_user(
        user_model: schemas.UserRegisterInfo,
        session: AsyncSession = Depends(get_session)
) -> schemas.SuccessMessageSend:
    try:
        new_user = await db.create_user(user_model, session)
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )
        
        send_verification_code.delay(new_user.email)
        return schemas.SuccessMessageSend(
            message="Verification code sent successfully",
        )
    except Exception as e:
        logging.exception("Failed to add new user")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't create user: {}".format(str(e))
        )


@router.post('/login')
async def auth_user(
        user_login_form_data: schemas.UserLoginInfo = Depends(get_user_login_schema),
) -> schemas.SuccessMessageSend:
    """
    first authorization router, user enter phone number and will receive 6-digits code
    :param user_login_form_data
    :return: success message
    :raise HTTPException with 500(some gone wrong)
    """
    try:
        send_verification_code.delay(user_login_form_data.email)
        return schemas.SuccessMessageSend(
            message="Send verification code successfully",
        )
    except Exception:
        logging.exception("Exception")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/verify_code")
async def verify_code(
        response: Response,
        user_auth_info: schemas.UserAuthInfo,
        session: AsyncSession = Depends(get_session)
) -> schemas.SuccessMessageSend:
    """
    Second authorization handler, user has received the code, and will enter it to form with code.
    Set cookies with access and refresh token with httpOnly.
    """
    redis_client = await get_redis()
    backend_code_from_user = await redis_client.get(user_auth_info.email)
    if backend_code_from_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Code lifetime is expired"
        )
    if not hmac.compare_digest(backend_code_from_user, str(user_auth_info.code)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Wrong code'
        )
    await redis_client.delete(user_auth_info.email)
    try:
        user: models.User = await db.get_user(user_auth_info.email, session)
    except Exception:
        logging.exception("Error while getting user during code verification")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong during code verification"
        )
    
    access_token: str = create_access_token(user=schemas.User(**user.__dict__))
    refresh_token: str = create_refresh_token(user.id)

    response.set_cookie(
        key=jwt_schemas.TokenType.access_token.value,
        value=access_token,
        httponly=True,
        secure=False,
    )
    response.set_cookie(
        key=jwt_schemas.TokenType.refresh_token.value,
        value=refresh_token,
        httponly=True,
        secure=False,
    )
    return schemas.SuccessMessageSend(
        message="Auth success, cookies were set!",
    )


@router.get("/refresh_token")
async def get_new_access_token(
        response: Response,
        user_id: int = Depends(get_user_id_from_refresh_token),
):
    """
    using to update access token
    :param response:
    :param user_id: user id from refresh token(token after validation)
    :return: None (set new access token in cookies)
    """
    # get user from database
    ### CRUD USER GETTER
    user = await db.get_user_by_id(user_id)  # Replace with your actual CRUD function
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

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
    """
    delete user cookies
    :param response:
    :param _: uses to check that user logged
    :return: None (delete both tokens cookies)
    """
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
    """
    random protected hand
    :param _: uses to check that user logged
    :return:
    """
    return {"status": "success"}
