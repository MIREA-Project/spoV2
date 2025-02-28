from dotenv import load_dotenv
from pydantic import BaseModel, field_validator, EmailStr
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class SMTPConfig(BaseModel):
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: EmailStr
    SMTP_PASSWORD: str


class AuthJWT(BaseModel):
    """
    base config for jwt information
    """
    public_key_path: str
    private_key_path: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    token_type_field: str


class Config(BaseModel):
    verification_code_time_expiration: int
    project_host: str
    jwt: AuthJWT
    smtp: SMTPConfig

    @field_validator("project_host")
    def validate_host(cls, value):
        if value.endswith("/"):
            raise Exception("Config: project_host should be without /")
        return value


def load_config() -> Config:
    """
    return config in modules that requires settings
    :return: config with all parameters
    """
    return Config(
        verification_code_time_expiration=60 * 5,
        project_host="http://localhost:8000",
        jwt=AuthJWT(
            public_key_path=Path(os.path.join(BASE_DIR, "certs", "jwt-public.pem")).read_text(),
            private_key_path=Path(os.path.join(BASE_DIR, "certs", "jwt-private.pem")).read_text(),
            algorithm="RS256",
            access_token_expire_minutes=5,
            refresh_token_expire_days=10,
            token_type_field="token_type"
        ),
        smtp=SMTPConfig(
            SMTP_SERVER=os.getenv("SMTP_SERVER"),
            SMTP_PORT=int(os.getenv("SMTP_PORT")),
            SMTP_USER=os.getenv("SMTP_USER"),
            SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
        )
    )
