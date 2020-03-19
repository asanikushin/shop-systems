from .types import *

from auth.models.users import User, Session
from auth import db
from constants import statuses

from flask import current_app

import jwt
import secrets
import datetime


class Storage:
    def __init__(self):
        self._db = db

    def add_user(self, email, password) -> STATUS:
        if self.has_email(email):
            return statuses["user"]["emailUsed"]

        user = User(email=email)
        user.set_password(password)
        self._db.session.add(user)
        self._db.session.commit()
        return statuses["user"]["created"]

    @staticmethod
    def has_email(email) -> bool:
        return User.query.filter(User.email == email).first() is not None

    @staticmethod
    def get_user(email) -> MODEL_TYPE:
        return User.query.filter(User.email == email).first()

    @staticmethod
    def check_user(email, password):
        user = Storage.get_user(email)
        return user.check_password(password)

    def create_session(self, email, password):
        if not self.has_email(email):
            return None, None, statuses["user"]["noUser"]

        if not self.check_user(email, password):
            return None, None, statuses["user"]["wrongPassword"]

        refresh_token = secrets.token_hex(64)
        access_token = str(jwt.encode(
            {"email": email, "exp": datetime.datetime.utcnow() + current_app.config["ACCESS_TOKEN_EXPIRATION"]},
            current_app.config["TOKENS_SECRET"]))

        session = Session(refreshToken=refresh_token,
                          refreshTokenExpireAt=datetime.datetime.utcnow() + current_app.config[
                              "REFRESH_TOKEN_EXPIRATION"])

        user = self.get_user(email)
        session.userId = user.id

        self._db.session.add(session)
        self._db.session.commit()
        return access_token, refresh_token, statuses["tokens"]["created"]

    def update_session(self, refresh_token):
        now = datetime.datetime.utcnow()
        session = Session.query.filter(Session.refreshToken == refresh_token).first()

        if session is None:
            return None, None, statuses["tokens"]["noSuchToken"]

        if now > session.refreshTokenExpireAt:
            return None, None, statuses["tokens"]["refreshTokenExpired"]
        user = User.query.get(session.userId)

        refresh_token = secrets.token_hex(64)
        access_token = str(jwt.encode(
            {"email": user.email, "exp": datetime.datetime.utcnow() + current_app.config["ACCESS_TOKEN_EXPIRATION"]},
            current_app.config["TOKENS_SECRET"], algorithm='HS256'))[2:-1]

        session.refreshToken = refresh_token
        session.refreshTokenExpireAt = datetime.datetime.utcnow() + current_app.config["REFRESH_TOKEN_EXPIRATION"]

        self._db.session.commit()
        return access_token, refresh_token, statuses["tokens"]["created"]

    @staticmethod
    def check_token(access_token):
        try:
            value = jwt.decode(access_token, current_app.config["TOKENS_SECRET"], algorithms=['HS256'])
        except jwt.ExpiredSignatureError as err:
            return err, statuses["tokens"]["accessTokenExpired"]
        return value, statuses["tokens"]["accessOk"]
