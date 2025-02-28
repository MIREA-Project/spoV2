from fastapi import Form, HTTPException
from starlette import status

from modules.reg_module import schemas


def get_user_login_schema(
        email: str = Form(...),
        password: str = Form(...),
) -> schemas.UserLoginInfo:
    try:
        return schemas.UserLoginInfo(email=email, password=password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid user creds"
        )
