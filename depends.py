import re

from fastapi import Form, HTTPException
from typing import Annotated

from pydantic import ValidationError

import schemas


def get_form_data(
        phone_number: Annotated[str, Form()]
) -> schemas.PhoneNumber:
    try:
        return schemas.PhoneNumber(
            phone_number=phone_number,
        )
    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid format of phone number",
        )


def validate_code(
        code: int,
        phone_number: str
) -> schemas.UserAuthInfo:
    try:
        return schemas.UserAuthInfo(
            phone_number=schemas.PhoneNumber(phone_number=phone_number),
            code=code,
        )
    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid format of code or phone number",
        )
