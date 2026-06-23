from fastapi.testclient import TestClient

from app.main import app
from app.repositories.categories import InMemoryCategoryRepository
from app.routes.categories import get_category_service
from app.services.categories import CategoryService


def make_client() -> TestClient:
    repository = InMemoryCategoryRepository()

    def override_category_service() -> CategoryService:
        return CategoryService(repository)

    app.dependency_overrides[get_category_service] = override_category_service
    return TestClient(app)


def test_list_categories_starts_empty():
    client = make_client()

    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_create_category_returns_created_category():
    client = make_client()
    payload = {
        "name": "Groceries",
        "color": "#12a150",
        "icon": "shopping-basket",
    }

    response = client.post("/categories", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]
    assert body["name"] == "Groceries"
    assert body["color"] == "#12a150"
    assert body["icon"] == "shopping-basket"
    assert body["is_archived"] is False

    app.dependency_overrides.clear()


def test_get_category_returns_existing_category():
    client = make_client()
    create_response = client.post(
        "/categories",
        json={
            "name": "Dining",
            "color": "#ff7a3d",
        },
    )

    response = client.get(f"/categories/{create_response.json()['id']}")

    assert response.status_code == 200
    assert response.json() == create_response.json()

    app.dependency_overrides.clear()


def test_get_missing_category_returns_404():
    client = make_client()

    response = client.get("/categories/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found."}

    app.dependency_overrides.clear()
