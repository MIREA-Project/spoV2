from pydantic import BaseModel, field_validator, EmailStr
import re


class SuccessMessageSend(BaseModel):
    message: str


class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str


class UserAuthInfo(BaseModel):
    code: int
    email: EmailStr

    @field_validator("code")
    def validate_code(cls, value):
        if not re.fullmatch(r"\d{6}", str(value)):
            raise ValueError("Code must be 6-digit number")
        return value


class UserLoginInfo(BaseModel):
    email: EmailStr
    password: str


class UserRegisterInfo(UserLoginInfo):
    nickname: str
