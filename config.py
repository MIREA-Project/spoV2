from pydantic import BaseModel


class Config(BaseModel):
    verification_code_time_expiration: int


def load_config() -> Config:
    return Config(
        verification_code_time_expiration=60 * 5
    )
