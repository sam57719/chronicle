from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.entrypoints.api.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provides a TestClient."""

    with TestClient(app) as c:
        yield c


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
