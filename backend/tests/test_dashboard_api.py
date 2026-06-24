from datetime import date

from fastapi.testclient import TestClient

from app.dependencies import get_dashboard_service
from app.main import app
from app.repositories.accounts import InMemoryAccountRepository
from app.repositories.categories import InMemoryCategoryRepository
from app.repositories.transactions import InMemoryTransactionRepository
from app.schemas.accounts import AccountCreate
from app.schemas.categories import CategoryCreate
from app.schemas.transactions import TransactionCreate
from app.services.dashboard import DashboardService


def make_client_with_repositories():
    transaction_repository = InMemoryTransactionRepository()
    account_repository = InMemoryAccountRepository()
    category_repository = InMemoryCategoryRepository()

    def override_dashboard_service() -> DashboardService:
        return DashboardService(
            transaction_repository,
            account_repository,
            category_repository,
        )

    app.dependency_overrides[get_dashboard_service] = override_dashboard_service
    return (
        TestClient(app),
        transaction_repository,
        account_repository,
        category_repository,
    )


def test_dashboard_summary_starts_empty():
    client, _, _, _ = make_client_with_repositories()

    response = client.get("/dashboard/summary?year=2026&month=6")

    assert response.status_code == 200
    assert response.json() == {
        "monthly_expenses": [],
        "top_categories": [],
        "recent_expenses": [],
    }

    app.dependency_overrides.clear()


def test_dashboard_summary_returns_monthly_category_and_recent_expenses():
    (
        client,
        transaction_repository,
        account_repository,
        category_repository,
    ) = make_client_with_repositories()
    account = account_repository.create(
        AccountCreate(
            name="Everyday Checking",
            account_type="checking",
            opening_balance_cents=10000,
        )
    )
    groceries = category_repository.create(
        CategoryCreate(
            name="Groceries",
            color="#12a150",
        )
    )
    dining = category_repository.create(
        CategoryCreate(
            name="Dining",
            color="#ff7a3d",
        )
    )
    transaction_repository.create(
        TransactionCreate(
            account_id=account.id,
            category_id=groceries.id,
            transaction_type="expense",
            amount_cents=5000,
            transaction_date=date(2026, 6, 20),
            merchant_name="Grocery Store",
            payment_method="card",
        )
    )
    transaction_repository.create(
        TransactionCreate(
            account_id=account.id,
            category_id=dining.id,
            transaction_type="expense",
            amount_cents=2500,
            transaction_date=date(2026, 6, 21),
            merchant_name="Cafe",
            payment_method="card",
        )
    )
    transaction_repository.create(
        TransactionCreate(
            account_id=account.id,
            category_id=groceries.id,
            transaction_type="expense",
            amount_cents=1000,
            transaction_date=date(2026, 5, 31),
            merchant_name="Previous Month",
            payment_method="card",
        )
    )
    transaction_repository.create(
        TransactionCreate(
            account_id=account.id,
            transaction_type="income",
            amount_cents=300000,
            transaction_date=date(2026, 6, 22),
            merchant_name="Payroll",
        )
    )

    response = client.get("/dashboard/summary?year=2026&month=6")

    assert response.status_code == 200
    body = response.json()
    assert body["monthly_expenses"] == [
        {
            "month": "2026-06",
            "spent_cents": 7500,
            "budget_cents": None,
            "currency": "USD",
        }
    ]
    assert body["top_categories"][0]["category_name"] == "Groceries"
    assert body["top_categories"][0]["spent_cents"] == 5000
    assert body["top_categories"][0]["percent_of_total"] == 5000 / 7500 * 100
    assert body["top_categories"][1]["category_name"] == "Dining"
    assert [expense["merchant_name"] for expense in body["recent_expenses"]] == [
        "Cafe",
        "Grocery Store",
        "Previous Month",
    ]
    assert body["recent_expenses"][0]["account_name"] == "Everyday Checking"
    assert body["recent_expenses"][0]["category_name"] == "Dining"

    app.dependency_overrides.clear()


def test_dashboard_summary_rejects_invalid_month():
    client, _, _, _ = make_client_with_repositories()

    response = client.get("/dashboard/summary?year=2026&month=13")

    assert response.status_code == 422

    app.dependency_overrides.clear()
