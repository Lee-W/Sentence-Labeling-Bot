from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


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


class SentenceSimilairty(db.Model):
    __tablename__ = 'sentence_similarity'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    paraphrase_id = db.Column(db.Integer, db.ForeignKey('paraphrase.id'))
    score = db.Column(db.Integer)


class SentenceBinary(db.Model):
    __tablename__ = 'sentence_binary'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    paraphrase_id = db.Column(db.Integer, db.ForeignKey('paraphrase.id'))
    is_similar = db.Column(db.Boolean)


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
        return check_password_hash(self.password, password)
