import logging
import random
import bcrypt

from email_sender_tasks.tasks import send_verification_code_by_smtp
from redis.asyncio import Redis

from core.config import load_config

config = load_config()


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password_to_check: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password_to_check.encode('utf-8'), password_hash.encode('utf-8'))


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
        print(f"Successfully sent verification code {code_to_user} to {email}")
        return code_to_user
    except Exception:
        logging.exception("Failed to send verification code")
