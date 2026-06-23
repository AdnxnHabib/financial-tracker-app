from typing import List

from app.repositories.accounts import InMemoryAccountRepository
from app.repositories.categories import InMemoryCategoryRepository
from app.repositories.transactions import InMemoryTransactionRepository
from app.schemas.transactions import (
    RecentTransactionRead,
    TransactionCreate,
    TransactionRead,
)


class TransactionService:
    def __init__(
        self,
        repository: InMemoryTransactionRepository,
        account_repository: InMemoryAccountRepository,
        category_repository: InMemoryCategoryRepository,
    ) -> None:
        self._repository = repository
        self._account_repository = account_repository
        self._category_repository = category_repository

    def create_transaction(self, transaction: TransactionCreate) -> TransactionRead:
        return self._repository.create(transaction)

    def list_transactions(self) -> List[TransactionRead]:
        return self._repository.list()

    def list_recent_transactions(self, limit: int) -> List[RecentTransactionRead]:
        transactions = self._repository.list_recent(limit)
        recent_transactions: List[RecentTransactionRead] = []

        for transaction in transactions:
            account = self._account_repository.get(transaction.account_id)
            category = (
                self._category_repository.get(transaction.category_id)
                if transaction.category_id is not None
                else None
            )
            recent_transactions.append(
                RecentTransactionRead(
                    **transaction.model_dump(),
                    account_name=account.name if account else "Unknown account",
                    category_name=category.name if category else None,
                )
            )

        return recent_transactions
