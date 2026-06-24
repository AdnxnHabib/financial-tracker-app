from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.schemas.transactions import (
    TransactionCreate,
    TransactionFilters,
    TransactionRead,
)


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._transactions: List[TransactionRead] = []

    def create(self, transaction: TransactionCreate) -> TransactionRead:
        now = datetime.now(timezone.utc)
        transaction_read = TransactionRead(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **transaction.model_dump(),
        )
        self._transactions.append(transaction_read)
        return transaction_read

    def list(self, filters: TransactionFilters) -> List[TransactionRead]:
        transactions = [
            transaction
            for transaction in self._transactions
            if self._matches_filters(transaction, filters)
        ]
        transactions = sorted(
            transactions,
            key=self._sort_key(filters.sort),
            reverse=self._sort_reverse(filters.sort),
        )
        return transactions[filters.offset : filters.offset + filters.limit]

    def list_all(self) -> List[TransactionRead]:
        return list(self._transactions)

    def _matches_filters(
        self,
        transaction: TransactionRead,
        filters: TransactionFilters,
    ) -> bool:
        if (
            filters.transaction_type is not None
            and transaction.transaction_type != filters.transaction_type
        ):
            return False
        if (
            filters.account_id is not None
            and transaction.account_id != filters.account_id
        ):
            return False
        if (
            filters.category_id is not None
            and transaction.category_id != filters.category_id
        ):
            return False
        if filters.status is not None and transaction.status != filters.status:
            return False
        if (
            filters.start_date is not None
            and transaction.transaction_date < filters.start_date
        ):
            return False
        if (
            filters.end_date is not None
            and transaction.transaction_date > filters.end_date
        ):
            return False
        if filters.search is not None:
            search = filters.search.casefold()
            merchant_name = transaction.merchant_name or ""
            description = transaction.description or ""
            if (
                search not in merchant_name.casefold()
                and search not in description.casefold()
            ):
                return False
        return True

    def _sort_key(self, sort: str):
        if sort in {"amount_asc", "amount_desc"}:
            return lambda transaction: transaction.amount_cents
        return lambda transaction: (
            transaction.transaction_date,
            transaction.created_at,
        )

    def _sort_reverse(self, sort: str) -> bool:
        return sort in {"recent", "amount_desc"}
