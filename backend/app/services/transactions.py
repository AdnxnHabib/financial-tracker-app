from typing import List

from app.repositories.transactions import InMemoryTransactionRepository
from app.schemas.transactions import TransactionCreate, TransactionRead


class TransactionService:
    def __init__(self, repository: InMemoryTransactionRepository) -> None:
        self._repository = repository

    def create_transaction(self, transaction: TransactionCreate) -> TransactionRead:
        return self._repository.create(transaction)

    def list_transactions(self) -> List[TransactionRead]:
        return self._repository.list()
