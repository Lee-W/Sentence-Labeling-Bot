from flask import current_app


def test_current_app_exists():
    assert current_app is not None


def test_app_exists(app):
    assert app is not None


def test_app_is_testing(app):
    assert app.config['TESTING']
