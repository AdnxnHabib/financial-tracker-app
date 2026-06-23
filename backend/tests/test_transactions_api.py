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
    body = list_response.json()
    assert len(body) == 1
    assert body[0]["id"] == create_response.json()["id"]
    assert body[0]["merchant_name"] == "Grocery Store"
    assert body[0]["account_name"] == "Unknown account"
    assert body[0]["category_name"] is None

    app.dependency_overrides.clear()


def test_list_transactions_sorts_recent_first_with_limit():
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

    response = client.get("/transactions?sort=recent&limit=2")

    assert response.status_code == 200
    body = response.json()
    assert [transaction["merchant_name"] for transaction in body] == [
        "Newest Store",
        "Middle Store",
    ]

    app.dependency_overrides.clear()


def test_list_transactions_resolves_account_and_category_names():
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
    response = client.get("/transactions?limit=1")

    assert create_response.status_code == 201
    assert response.status_code == 200
    assert response.json()[0]["account_name"] == "Everyday Checking"
    assert response.json()[0]["category_name"] == "Groceries"

    app.dependency_overrides.clear()


def test_list_transactions_defaults_to_twenty_results():
    client = make_client()

    for index in range(21):
        create_response = client.post(
            "/transactions",
            json={
                "account_id": "11111111-1111-1111-1111-111111111111",
                "category_id": "22222222-2222-2222-2222-222222222222",
                "transaction_type": "expense",
                "amount_cents": 1000 + index,
                "transaction_date": f"2026-06-{(index % 20) + 1:02d}",
                "merchant_name": f"Store {index}",
            },
        )
        assert create_response.status_code == 201

    response = client.get("/transactions")

    assert response.status_code == 200
    assert len(response.json()) == 20

    app.dependency_overrides.clear()


def test_list_transactions_filters_by_type_status_date_range_and_search():
    client = make_client()
    payloads = [
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "category_id": "22222222-2222-2222-2222-222222222222",
            "transaction_type": "expense",
            "amount_cents": 1200,
            "transaction_date": "2026-06-18",
            "merchant_name": "Coffee Bar",
            "status": "cleared",
        },
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "category_id": "22222222-2222-2222-2222-222222222222",
            "transaction_type": "expense",
            "amount_cents": 7500,
            "transaction_date": "2026-06-20",
            "merchant_name": "Grocery Store",
            "description": "Weekly groceries",
            "status": "cleared",
        },
        {
            "account_id": "11111111-1111-1111-1111-111111111111",
            "transaction_type": "income",
            "amount_cents": 300000,
            "transaction_date": "2026-06-21",
            "merchant_name": "Payroll",
            "status": "pending",
        },
    ]

    for payload in payloads:
        create_response = client.post("/transactions", json=payload)
        assert create_response.status_code == 201

    response = client.get(
        "/transactions"
        "?transaction_type=expense"
        "&status=cleared"
        "&start_date=2026-06-19"
        "&end_date=2026-06-21"
        "&search=groceries"
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["merchant_name"] == "Grocery Store"

    app.dependency_overrides.clear()


def test_list_transactions_uses_offset_for_pagination():
    client = make_client()

    for index in range(3):
        create_response = client.post(
            "/transactions",
            json={
                "account_id": "11111111-1111-1111-1111-111111111111",
                "category_id": "22222222-2222-2222-2222-222222222222",
                "transaction_type": "expense",
                "amount_cents": 1000 + index,
                "transaction_date": f"2026-06-{index + 20}",
                "merchant_name": f"Store {index}",
            },
        )
        assert create_response.status_code == 201

    response = client.get("/transactions?sort=oldest&limit=1&offset=1")

    assert response.status_code == 200
    assert response.json()[0]["merchant_name"] == "Store 1"

    app.dependency_overrides.clear()


def test_list_transactions_rejects_invalid_limit():
    client = make_client()

    response = client.get("/transactions?limit=0")

    assert response.status_code == 422

    app.dependency_overrides.clear()


def test_recent_transactions_endpoint_is_removed():
    client = make_client()

    response = client.get("/transactions/recent")

    assert response.status_code == 404

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
