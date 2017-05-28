import pytest

from labelingbot import create_app
from labelingbot import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')

    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    db.session.begin(subtransactions=True)

    yield db.session

    db.session.rollback()
    db.session.remove()


@pytest.fixture(scope='session')
def client(app):
    _client = app.test_client(use_cookies=True)
    return _client
