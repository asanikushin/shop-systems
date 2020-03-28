from .types import *

from auth.models.users import User, Session
from auth import db
from constants import statuses
from utils.checkers import check_email
from utils.queues import send_message

from flask import current_app

import jwt
import json
import secrets
import datetime


class Storage:
    def __init__(self):
        self._db = db

    def add_user(self, email, password) -> STATUS:
        if self.has_email(email):
            return statuses["user"]["emailUsed"]

        if not (email := check_email(email)):
            return statuses["user"]["invalidEmail"]

        user = User(email=email)
        user.set_password(password)
        user.confirmed = False

        send_message(current_app.config["RABBITMQ"], current_app.config["QUEUE"],
                     json.dumps(dict(email=email, text=f"To confirm go to {self.create_confirm_link(user)}",
                                     subject="Conformation email")))

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
    def check_user(email, password) -> bool:
        user = Storage.get_user(email)
        return user.check_password(password)

    def create_session(self, email, password):
        if not self.has_email(email):
            return None, None, statuses["user"]["noUser"]

        if not self.check_user(email, password):
            return None, None, statuses["user"]["wrongPassword"]

        user = self.get_user(email)

        if not user.confirmed:
            send_message(current_app.config["RABBITMQ"], current_app.config["QUEUE"],
                         json.dumps(dict(email=email, text=f"To confirm go to {self.create_confirm_link(user)}")))
            return None, None, statuses["user"]["notConfirmed"]

        session = Session(userId=user.id)
        return self.save_session(email, session)

    def update_session(self, refresh_token):
        now = datetime.datetime.utcnow()
        session = Session.query.filter(Session.refreshToken == refresh_token).first()

        if session is None:
            return None, None, statuses["tokens"]["noSuchToken"]

        if now > session.refreshTokenExpireAt:
            return None, None, statuses["tokens"]["refreshTokenExpired"]

        user = User.query.get(session.userId)
        new_session = Session(userId=user.id)
        response = self.save_session(user.email, new_session)

        self._delete_session(session)
        return response

    @staticmethod
    def check_token(access_token):
        try:
            value = jwt.decode(access_token, current_app.config["TOKENS_SECRET"], algorithms=['HS256'])
        except jwt.ExpiredSignatureError as err:
            return err, statuses["tokens"]["accessTokenExpired"]
        except jwt.DecodeError as err:
            return err, statuses["tokens"]["invalidToken"]
        session_id = value["session"]
        session = Session.query.get(session_id)
        if session is None:
            return "Related session was removed", statuses["tokens"]["invalidToken"]
        return value, statuses["tokens"]["accessOk"]

    @staticmethod
    def create_tokens(email, session: Session, time=datetime.datetime.utcnow()):
        refresh_token = secrets.token_hex(64)
        access_token = str(jwt.encode(
            {"email": email, "session": session.id,
             "exp": time + current_app.config["ACCESS_TOKEN_EXPIRATION"]},
            current_app.config["TOKENS_SECRET"]))[2:-1]

        return access_token, refresh_token

    @staticmethod
    def create_confirm_link(user: User):
        token = str(jwt.encode({"email": user.email, "id": user.id}, current_app.config["TOKENS_SECRET"]))[2:-1]
        return f"http://localhost:8082/confirm/{token}"

    def save_session(self, email, session: Session):
        self._db.session.add(session)
        self._db.session.commit()

        now = datetime.datetime.utcnow()
        access_token, refresh_token = self.create_tokens(email, session, now)
        session.refreshToken = refresh_token
        session.refreshTokenExpireAt = now + current_app.config["REFRESH_TOKEN_EXPIRATION"]
        self._db.session.commit()
        return access_token, refresh_token, statuses["tokens"]["created"]

    def _delete_session(self, session):
        self._db.session.delete(session)
        self._db.session.commit()

    def confirm_user(self, token):
        try:
            value = jwt.decode(token, current_app.config["TOKENS_SECRET"], algorithms=['HS256'])
        except jwt.DecodeError as err:
            return err, statuses["tokens"]["invalidToken"]
        user = User.query.get(value["id"])
        user.confirmed = True
        self._db.session.commit()

        return None, statuses["user"]["confirmed"]
