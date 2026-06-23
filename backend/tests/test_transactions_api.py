from fastapi.testclient import TestClient

from app.main import app
from app.repositories.accounts import InMemoryAccountRepository
from app.repositories.categories import InMemoryCategoryRepository
from app.repositories.transactions import InMemoryTransactionRepository
from app.routes.transactions import get_transaction_service
from app.schemas.accounts import AccountCreate
from app.schemas.categories import CategoryCreate
from app.services.transactions import TransactionService


def make_client() -> TestClient:
    transaction_repository = InMemoryTransactionRepository()
    account_repository = InMemoryAccountRepository()
    category_repository = InMemoryCategoryRepository()

    def override_transaction_service() -> TransactionService:
        return TransactionService(
            transaction_repository,
            account_repository,
            category_repository,
        )

    app.dependency_overrides[get_transaction_service] = override_transaction_service
    return TestClient(app)


def make_client_with_repositories():
    transaction_repository = InMemoryTransactionRepository()
    account_repository = InMemoryAccountRepository()
    category_repository = InMemoryCategoryRepository()

    def override_transaction_service() -> TransactionService:
        return TransactionService(
            transaction_repository,
            account_repository,
            category_repository,
        )

    app.dependency_overrides[get_transaction_service] = override_transaction_service
    return TestClient(app), account_repository, category_repository


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


def test_list_recent_transactions_returns_newest_first_with_limit():
    client = make_client()
    payloads = [
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "category_id": "22222222-2222-2222-2222-222222222222",
            "transaction_type": "expense",
            "amount_cents": 1000,
            "transaction_date": "2026-06-20",
            "merchant_name": "Older Store",
        },
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "category_id": "22222222-2222-2222-2222-222222222222",
            "transaction_type": "expense",
            "amount_cents": 2000,
            "transaction_date": "2026-06-22",
            "merchant_name": "Newest Store",
        },
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "category_id": "22222222-2222-2222-2222-222222222222",
            "transaction_type": "expense",
            "amount_cents": 1500,
            "transaction_date": "2026-06-21",
            "merchant_name": "Middle Store",
        },
    ]

    for payload in payloads:
        create_response = client.post("/transactions", json=payload)
        assert create_response.status_code == 201

    response = client.get("/transactions/recent?limit=2")

    assert response.status_code == 200
    body = response.json()
    assert [transaction["merchant_name"] for transaction in body] == [
        "Newest Store",
        "Middle Store",
    ]

    app.dependency_overrides.clear()


def test_list_recent_transactions_resolves_account_and_category_names():
    client, account_repository, category_repository = make_client_with_repositories()
    account = account_repository.create(
        AccountCreate(
            name="Everyday Checking",
            account_type="checking",
            opening_balance_cents=10000,
        )
    )
    category = category_repository.create(
        CategoryCreate(
            name="Groceries",
            color="#12a150",
            icon="shopping-basket",
        )
    )

    create_response = client.post(
        "/transactions",
        json={
            "account_id": str(account.id),
            "category_id": str(category.id),
            "transaction_type": "expense",
            "amount_cents": 2500,
            "transaction_date": "2026-06-22",
            "merchant_name": "Grocery Store",
        },
    )
    response = client.get("/transactions/recent?limit=1")

    assert create_response.status_code == 201
    assert response.status_code == 200
    assert response.json()[0]["account_name"] == "Everyday Checking"
    assert response.json()[0]["category_name"] == "Groceries"

    app.dependency_overrides.clear()


def test_list_recent_transactions_defaults_to_five_results():
    client = make_client()

    for index in range(6):
        create_response = client.post(
            "/transactions",
            json={
                "account_id": "11111111-1111-1111-1111-111111111111",
                "category_id": "22222222-2222-2222-2222-222222222222",
                "transaction_type": "expense",
                "amount_cents": 1000 + index,
                "transaction_date": f"2026-06-{index + 10}",
                "merchant_name": f"Store {index}",
            },
        )
        assert create_response.status_code == 201

    response = client.get("/transactions/recent")

    assert response.status_code == 200
    assert len(response.json()) == 5

    app.dependency_overrides.clear()


def test_list_recent_transactions_rejects_invalid_limit():
    client = make_client()

    response = client.get("/transactions/recent?limit=0")

    assert response.status_code == 422

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
