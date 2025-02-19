import logging
import random

from redis.asyncio import Redis

from .core.config import Config, load_config

config: Config = load_config()


def create_verification_code() -> int:
    return random.randint(100_000, 999_999)


async def send_verification_code(
        phone_number: str,
        redis: Redis
) -> int:
    code_to_user = create_verification_code()
    # imitate sms
    try:
        await redis.setex(
            name=phone_number,
            time=config.verification_code_time_expiration,
            value=code_to_user
        )
        print(f"Successfully sent verification code {code_to_user} to {phone_number}")
        return code_to_user
    except Exception as err:
        logging.exception("Failed to send verification code")
