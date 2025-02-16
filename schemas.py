from pydantic import BaseModel, field_validator
import re


class PhoneNumber(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        assert re.fullmatch(r"\+7\d{10}", value)
        return value


class SuccessMessageSend(BaseModel):
    message: str


class UserAuthInfo(BaseModel):
    code: int
    phone_number: PhoneNumber

    @field_validator("code")
    def validate_phone_number(cls, value):
        assert re.fullmatch(r"\d{6}", str(value))
        return value
