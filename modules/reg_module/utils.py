import logging
import random

from email_sender_tasks.tasks import send_verification_code_by_smtp
from redis.asyncio import Redis

from core.config import load_config

config = load_config()


def create_verification_code() -> int:
    """
    simple verification code creator
    :return:
    """
    return random.randint(100_000, 999_999)


async def send_verification_code(
        email: str,
        redis: Redis
) -> int:
    """
    imitate smtp sender code
    :param email: validated user email
    :param redis: async redis client
    :return: verification code
    """
    code_to_user = create_verification_code()
    # imitate sms
    try:
        await redis.setex(
            name=email,
            time=config.verification_code_time_expiration,
            value=code_to_user
        )
        send_verification_code_by_smtp(
            email=email,
            auth_code=code_to_user
        )
        # print(f"Successfully sent verification code {code_to_user} to {phone_number}")
        return code_to_user
    except Exception:
        logging.exception("Failed to send verification code")
