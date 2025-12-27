import pytest
from fastapi.testclient import TestClient
from app.entrypoints.api.main import app
from app.entrypoints.api.v1.items.dependencies import get_item_repository
from app.features.items.infrastructure.repositories import InMemoryItemRepository


@pytest.fixture
def client():
    """Provides a TestClient and clears the repository before each test."""
    # 1. Create a fresh repository instance
    test_repo = InMemoryItemRepository()

    # 2. Tell FastAPI to use this fresh repo instead of the cached one
    app.dependency_overrides[get_item_repository] = lambda: test_repo

    with TestClient(app) as c:
        yield c

    # 3. Clean up the override after the test finishes
    app.dependency_overrides.clear()


def test_create_item_success(client):
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


def test_create_item_invalid_data(client):
    # Act: Send empty name (which our Domain/Schema forbids)
    response = client.post("/api/v1/items/", json={"name": ""})

    # Assert
    # Note: If Pydantic catches it, it's 422. If your Domain catches it, it's 400.
    assert response.status_code in (400, 422)


def test_list_items_returns_list(client):
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


def test_get_specific_item(client):
    # Arrange: Create an item to get its ID
    created = client.post("/api/v1/items/", json={"name": "Specific Item"}).json()
    item_id = created["id"]

    # Act
    response = client.get(f"/api/v1/items/{item_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Specific Item"


def test_get_nonexistent_item_returns_404(client):
    # Act: Use a valid UUID format that doesn't exist
    fake_id = "019b388f-4d65-7325-8c6a-b13255595291"
    response = client.get(f"/api/v1/items/{fake_id}")

    # Assert
    assert response.status_code == 404
