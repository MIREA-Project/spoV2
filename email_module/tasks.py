import smtplib
from email.mime.text import MIMEText
from core.celery_config import celery
from core.config import load_config
import logging

config = load_config()


@celery.task
def send_verification_code_by_smtp(email: str, auth_code: int) -> None:
    """
    отправляет код по email

    :param auth_code: 6-digits code
    :param email: user validated email
    :return:
    """
    # Создаем email-сообщение
    msg = MIMEText(f"Ваш код подтверждения: {auth_code}")
    msg["Subject"] = "Код подтверждения"
    msg["From"] = config.smtp.SMTP_USER
    msg["To"] = email

    # Отправляем email
    try:
        with smtplib.SMTP(
                config.smtp.SMTP_SERVER,
                config.smtp.SMTP_PORT
        ) as server:
            server.starttls()
            server.login(config.smtp.SMTP_USER, config.smtp.SMTP_PASSWORD)
            server.sendmail(config.smtp.SMTP_USER, email, msg.as_string())
    except Exception:
        logging.exception("Error while sending verification code")
