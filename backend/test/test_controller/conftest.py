import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.api.dependencies import get_duck, get_pg
from app.api.fast_api import app


@pytest.fixture()
def mock_pg():
    return MagicMock()


@pytest.fixture()
def mock_duck():
    mock = MagicMock()
    mock.execute.return_value.fetchall.return_value = []
    return mock


@pytest.fixture()
def client(mock_pg, mock_duck):
    app.dependency_overrides[get_pg] = lambda: mock_pg
    app.dependency_overrides[get_duck] = lambda: mock_duck
    yield TestClient(app)
    app.dependency_overrides.clear()
