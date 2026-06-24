from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from app.repositories.accounts import InMemoryAccountRepository
from app.repositories.categories import InMemoryCategoryRepository
from app.repositories.transactions import InMemoryTransactionRepository
from app.schemas.common import CurrencyCode, TransactionType
from app.schemas.dashboard import (
    CategorySpendRead,
    DashboardRead,
    MonthlyExpenseRead,
    RecentExpenseRead,
)
from app.schemas.transactions import TransactionRead


class DashboardService:
    def __init__(
        self,
        transaction_repository: InMemoryTransactionRepository,
        account_repository: InMemoryAccountRepository,
        category_repository: InMemoryCategoryRepository,
    ) -> None:
        self._transaction_repository = transaction_repository
        self._account_repository = account_repository
        self._category_repository = category_repository

    def get_summary(
        self,
        *,
        year: Optional[int] = None,
        month: Optional[int] = None,
    ) -> DashboardRead:
        today = date.today()
        selected_year = year if year is not None else today.year
        selected_month = month if month is not None else today.month
        month_label = f"{selected_year:04d}-{selected_month:02d}"

        transactions = self._transaction_repository.list_all()
        month_expenses = [
            transaction
            for transaction in transactions
            if self._is_expense_in_month(transaction, selected_year, selected_month)
        ]

        return DashboardRead(
            monthly_expenses=self._build_monthly_expenses(
                month_expenses,
                month_label,
            ),
            top_categories=self._build_top_categories(month_expenses),
            recent_expenses=self._build_recent_expenses(transactions),
        )

    def _is_expense_in_month(
        self,
        transaction: TransactionRead,
        year: int,
        month: int,
    ) -> bool:
        return (
            transaction.transaction_type == TransactionType.EXPENSE
            and transaction.transaction_date.year == year
            and transaction.transaction_date.month == month
        )

    def _build_monthly_expenses(
        self,
        transactions: List[TransactionRead],
        month_label: str,
    ) -> List[MonthlyExpenseRead]:
        totals_by_currency: Dict[CurrencyCode, int] = defaultdict(int)
        for transaction in transactions:
            totals_by_currency[transaction.currency] += transaction.amount_cents

        return [
            MonthlyExpenseRead(
                month=month_label,
                spent_cents=spent_cents,
                budget_cents=None,
                currency=currency,
            )
            for currency, spent_cents in totals_by_currency.items()
        ]

    def _build_top_categories(
        self,
        transactions: List[TransactionRead],
    ) -> List[CategorySpendRead]:
        totals_by_currency: Dict[CurrencyCode, int] = defaultdict(int)
        totals_by_category: Dict[Tuple[UUID, CurrencyCode], int] = defaultdict(int)

        for transaction in transactions:
            if transaction.category_id is None:
                continue
            totals_by_currency[transaction.currency] += transaction.amount_cents
            totals_by_category[
                (transaction.category_id, transaction.currency)
            ] += transaction.amount_cents

        category_spend: List[CategorySpendRead] = []
        for (category_id, currency), spent_cents in totals_by_category.items():
            category = self._category_repository.get(category_id)
            total_for_currency = totals_by_currency[currency]
            percent_of_total = (
                spent_cents / total_for_currency * 100
                if total_for_currency > 0
                else 0
            )
            category_spend.append(
                CategorySpendRead(
                    category_id=category_id,
                    category_name=category.name if category else "Unknown category",
                    color=category.color if category else "#4f5cf6",
                    spent_cents=spent_cents,
                    percent_of_total=percent_of_total,
                    currency=currency,
                )
            )

        return sorted(
            category_spend,
            key=lambda category: category.spent_cents,
            reverse=True,
        )[:5]

    def _build_recent_expenses(
        self,
        transactions: List[TransactionRead],
    ) -> List[RecentExpenseRead]:
        expenses = [
            transaction
            for transaction in transactions
            if transaction.transaction_type == TransactionType.EXPENSE
        ]
        expenses = sorted(
            expenses,
            key=lambda transaction: (
                transaction.transaction_date,
                transaction.created_at,
            ),
            reverse=True,
        )

        return [
            RecentExpenseRead(
                id=transaction.id,
                merchant_name=transaction.merchant_name,
                category_name=self._category_name(transaction),
                account_name=self._account_name(transaction),
                amount_cents=transaction.amount_cents,
                currency=transaction.currency,
                transaction_date=transaction.transaction_date,
                payment_method=transaction.payment_method,
            )
            for transaction in expenses[:5]
        ]

    def _account_name(self, transaction: TransactionRead) -> str:
        account = self._account_repository.get(transaction.account_id)
        return account.name if account else "Unknown account"

    def _category_name(self, transaction: TransactionRead) -> str:
        if transaction.category_id is None:
            return "Uncategorized"
        category = self._category_repository.get(transaction.category_id)
        return category.name if category else "Unknown category"
