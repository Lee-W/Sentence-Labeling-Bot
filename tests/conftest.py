import pytest
from flask import current_app

from labelingbot import create_app


@pytest.fixture
def app():
    app = create_app('testing')
    return app


def test_app_exists():
    assert current_app is not None
