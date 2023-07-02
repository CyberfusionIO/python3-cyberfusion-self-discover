import pytest
from fastapi.testclient import TestClient

from self_discover.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
