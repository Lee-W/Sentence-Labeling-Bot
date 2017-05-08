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
