from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.entrypoints.api.main import create_app
from app.entrypoints.api.v1.items.dependencies import get_item_repository
from app.features.items.persistence.in_memory_repository import InMemoryItemRepository


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provides a TestClient and clears the repository before each test."""

    test_repo = InMemoryItemRepository()

    app = create_app()
    app.dependency_overrides[get_item_repository] = lambda: test_repo

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_create_item_success(client: TestClient) -> None:
    # Act
    response = client.post(
        "/api/v1/items/",
        json={"name": "Vintage Laserdisc", "description": "TOS - The Menagerie"},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vintage Laserdisc"
    assert "id" in data
    assert data["description"] == "TOS - The Menagerie"


def test_create_item_invalid_data(client: TestClient) -> None:
    # Act: Send empty name (which our Domain/Schema forbids)
    response = client.post("/api/v1/items/", json={"name": ""})

    # Assert
    # Note: If Pydantic catches it, it's 422. If your Domain catches it, it's 400.
    assert response.status_code in (400, 422)


def test_list_items_returns_list(client: TestClient) -> None:
    # Arrange: Create an item first
    client.post("/api/v1/items/", json={"name": "Item 1"})

    # Act
    response = client.get("/api/v1/items/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Item 1"


def test_get_specific_item(client: TestClient) -> None:
    # Arrange: Create an item to get its ID
    created = client.post("/api/v1/items/", json={"name": "Specific Item"}).json()
    item_id = created["id"]

    # Act
    response = client.get(f"/api/v1/items/{item_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Item"


def test_get_nonexistent_item_returns_404(client: TestClient) -> None:
    # Act: Use a valid UUID format that doesn't exist
    fake_id = "019b388f-4d65-7325-8c6a-b13255595291"
    response = client.get(f"/api/v1/items/{fake_id}")

    # Assert
    assert response.status_code == 404


def test_get_item_with_malformed_uuid_returns_400(client: TestClient) -> None:
    response = client.get("/api/v1/items/completely-wrong-format")

    assert response.status_code == 400
    assert "is not a valid UUID" in response.json()["detail"]


def test_delete_item(client: TestClient) -> None:
    # Arrange: Create an item to get its ID
    created = client.post("/api/v1/items/", json={"name": "Specific Item"}).json()
    item_id = created["id"]

    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204

    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404


def test_delete_item_with_malformed_uuid_returns_400(client: TestClient) -> None:
    response = client.delete("/api/v1/items/completely-wrong-format")
    assert response.status_code == 400


def test_delete_nonexistent_item_returns_404(client: TestClient) -> None:
    fake_id = "019b388f-4d65-7325-8c6a-b13255595291"
    response = client.delete(f"/api/v1/items/{fake_id}")
    assert response.status_code == 404
