# tests/conftest.py
import pytest
import sys
import os

from src.services.planet_service import PlanetService

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app as flask_app
from src.services.character_service import CharacterService

@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sw_service():
    return CharacterService()

@pytest.fixture
def planet_serv():
    return PlanetService()

@pytest.fixture(autouse=True)
def mock_env_vars():
    os.environ['API_KEY'] = 'test-secret-key'