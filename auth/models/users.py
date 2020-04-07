from auth import db

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    confirmed = db.Column(db.Boolean())
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}: {}>'.format(self.id, self.email)

    def get_dict(self):
        return dict(id=self.id, email=self.email)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    refreshToken = db.Column(db.Text)
    refreshTokenExpireAt = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Session {}: {} at {}>'.format(self.userId, self.refreshToken, self.refreshTokenExpireAt)

    def get_dict(self):
        return dict(refreshToken=self.refreshToken, refreshTokenExpireAt=self.refreshTokenExpireAt, userId=self.userId)
