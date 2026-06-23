from fastapi.testclient import TestClient

from app.main import app
from app.repositories.accounts import InMemoryAccountRepository
from app.routes.accounts import get_account_service
from app.services.accounts import AccountService


def make_client() -> TestClient:
    repository = InMemoryAccountRepository()

    def override_account_service() -> AccountService:
        return AccountService(repository)

    app.dependency_overrides[get_account_service] = override_account_service
    return TestClient(app)


def test_list_accounts_starts_empty():
    client = make_client()

    response = client.get("/accounts")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_create_account_returns_created_account():
    client = make_client()
    payload = {
        "name": "Everyday Checking",
        "account_type": "checking",
        "currency": "USD",
        "institution_name": "Chase",
        "opening_balance_cents": 250000,
    }

    response = client.post("/accounts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]
    assert body["name"] == "Everyday Checking"
    assert body["account_type"] == "checking"
    assert body["institution_name"] == "Chase"
    assert body["current_balance_cents"] == 250000
    assert "opening_balance_cents" not in body

    app.dependency_overrides.clear()


def test_get_account_returns_existing_account():
    client = make_client()
    create_response = client.post(
        "/accounts",
        json={
            "name": "Savings",
            "account_type": "savings",
            "opening_balance_cents": 10000,
        },
    )

    response = client.get(f"/accounts/{create_response.json()['id']}")

    assert response.status_code == 200
    assert response.json() == create_response.json()

    app.dependency_overrides.clear()


def test_get_missing_account_returns_404():
    client = make_client()

    response = client.get("/accounts/11111111-1111-1111-1111-111111111111")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account not found."}

    app.dependency_overrides.clear()
