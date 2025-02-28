import datetime

from .. import schemas
from . import jwt_schemas
from core.config import load_config

import jwt

config = load_config()


def create_access_token(
        user: schemas.User,
) -> str:
    """
    function creates access token using user payload
    :param user: user schema, not orm model
    :return: signed jwt access token(with use payload)
    """
    now = datetime.datetime.now(datetime.UTC)
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": now + datetime.timedelta(
            minutes=config.jwt.access_token_expire_minutes
        ),
        "nickname" : user.nickname,
        "iat": now,
        config.jwt.token_type_field: jwt_schemas.TokenType.access_token.value,
    }
    return jwt.encode(
        payload=jwt_payload,
        key=config.jwt.private_key_path,
        algorithm=config.jwt.algorithm,
    )


def create_refresh_token(
        user_id: int
) -> str:
    """
    function update access token using user id
    :param user_id: uses for jwt sub
    :return: signed refresh jwt token
    """
    now = datetime.datetime.now(datetime.UTC)
    jwt_payload = {
        "sub": str(user_id),
        config.jwt.token_type_field: jwt_schemas.TokenType.refresh_token.value,
        "exp": now + datetime.timedelta(
            days=config.jwt.refresh_token_expire_days
        ),
    }
    return jwt.encode(
        payload=jwt_payload,
        key=config.jwt.private_key_path,
        algorithm=config.jwt.algorithm,
    )
