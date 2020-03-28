import logging
import os


class BaseConfig:
    SMTP_URL = os.environ.get('SMTP_URL') or '127.0.0.1'
    SMTP_PORT = os.environ.get('SMTP_PORT') or '25'
    SMTP_URI = SMTP_URL + ":" + SMTP_PORT

    FROM_EMAIL = os.environ.get("FROM_EMAIL")

    RABBITMQ = os.environ.get("RABBITMQ")
    QUEUE = os.environ.get("QUEUE")

    LOG_LEVEL = logging.DEBUG
