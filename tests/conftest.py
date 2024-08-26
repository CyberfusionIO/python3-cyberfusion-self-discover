import pytest
from fastapi.testclient import TestClient

from cyberfusion.SelfDiscover.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
