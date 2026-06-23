from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from app.schemas.transactions import TransactionCreate, TransactionRead


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

    def list(self) -> List[TransactionRead]:
        return list(self._transactions)

    def list_recent(self, limit: int) -> List[TransactionRead]:
        transactions = sorted(
            self._transactions,
            key=lambda transaction: (
                transaction.transaction_date,
                transaction.created_at,
            ),
            reverse=True,
        )
        return transactions[:limit]
