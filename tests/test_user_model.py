import pytest

from labelingbot.models import User


@pytest.fixture(scope='function')
def user(session):
    user = User(name='test user', password='test password')

    session.add(user)
    session.commit()
    return user


def test_verify_password_success(user):
    assert user.verify_passowrd('test password')


def test_verify_password_failed(user):
    assert not user.verify_passowrd('not password')


def test_password_getter_failed(user):
    with pytest.raises(AttributeError):
        password = user.password


def test_password_setter_success(user):
    assert user.password_hash
