from goodsongs.factory import create_app
import pytest


@pytest.fixture
def app():
    app = create_app('../config/test.py')
    return app
