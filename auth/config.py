from utils.times import parse_timedelta

import datetime
import logging
import os

app_dir = os.path.abspath(os.path.dirname(__name__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(app_dir, 'app.db')

    ACCESS_TOKEN_EXPIRATION = parse_timedelta(os.environ.get('ACCESS_TOKEN_EXPIRATION')) or datetime.timedelta(
        minutes=5)
    REFRESH_TOKEN_EXPIRATION = parse_timedelta(os.environ.get('REFRESH_TOKEN_EXPIRATION')) or datetime.timedelta(
        minutes=5)
    TOKENS_SECRET = os.environ.get('TOKEN_SECRET') or '2816e66cb08c9f4cb5d7c080b2fca85f17cdb1cbe32380c7fdde9cf469185e30'
    CONFIRM_URL = os.environ.get('CONFIRM_URL')

    RABBITMQ = os.environ.get("RABBITMQ")
    QUEUE = os.environ.get("QUEUE")

    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = logging.INFO
