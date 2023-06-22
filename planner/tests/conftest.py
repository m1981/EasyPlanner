import pytest
from app import create_app

@pytest.fixture(scope='session')
def test_app():
    app = create_app()
    app.config['TESTING'] = True
    return app

