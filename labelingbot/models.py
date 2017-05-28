from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Sentence(db.Model):
    __tablename__ = 'sentence'
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String)
    content = db.Column(db.String)


class Paraphrase(db.Model):
    __tablename__ = 'paraphrase'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class SentenceSimilairty(db.Model):
    __tablename__ = 'sentence_similarity'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    paraphrase_id = db.Column(db.Integer, db.ForeignKey('paraphrase.id'))
    score = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class SentenceBinary(db.Model):
    __tablename__ = 'sentence_binary'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    paraphrase_id = db.Column(db.Integer, db.ForeignKey('paraphrase.id'))
    is_similar = db.Column(db.Boolean)
    created_by = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_passowrd(self, password):
        return check_password_hash(self.password_hash, password)


class TelegramUser(db.Model):
    __tablename__ = 'telegram_user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64))
    type = db.String(db.String(64))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
