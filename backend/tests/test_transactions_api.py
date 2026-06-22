from fastapi.testclient import TestClient

from app.main import app
from app.repositories.transactions import InMemoryTransactionRepository
from app.routes.transactions import get_transaction_service
from app.services.transactions import TransactionService


def make_client() -> TestClient:
    repository = InMemoryTransactionRepository()

    def override_transaction_service() -> TransactionService:
        return TransactionService(repository)

    app.dependency_overrides[get_transaction_service] = override_transaction_service
    return TestClient(app)


def test_list_transactions_starts_empty():
    client = make_client()

    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


def test_create_transaction_returns_created_transaction():
    client = make_client()
    payload = {
        "account_id": "11111111-1111-1111-1111-111111111111",
        "category_id": "22222222-2222-2222-2222-222222222222",
        "transaction_type": "expense",
        "amount_cents": 1299,
        "transaction_date": "2026-06-22",
        "merchant_name": "Test Merchant",
        "payment_method": "card",
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]
    assert body["amount_cents"] == 1299
    assert body["currency"] == "USD"
    assert body["merchant_name"] == "Test Merchant"
    assert body["status"] == "cleared"

    app.dependency_overrides.clear()


def test_created_transaction_appears_in_list():
    client = make_client()
    payload = {
        "account_id": "11111111-1111-1111-1111-111111111111",
        "category_id": "22222222-2222-2222-2222-222222222222",
        "transaction_type": "expense",
        "amount_cents": 2500,
        "transaction_date": "2026-06-22",
        "merchant_name": "Grocery Store",
    }

    create_response = client.post("/transactions", json=payload)
    list_response = client.get("/transactions")

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert list_response.json() == [create_response.json()]

    app.dependency_overrides.clear()


def test_expense_transaction_requires_category():
    client = make_client()
    payload = {
        "account_id": "11111111-1111-1111-1111-111111111111",
        "transaction_type": "expense",
        "amount_cents": 1299,
        "transaction_date": "2026-06-22",
    }

    response = client.post("/transactions", json=payload)

    assert response.status_code == 422
    assert "Expense transactions require a category_id" in response.text

    app.dependency_overrides.clear()
