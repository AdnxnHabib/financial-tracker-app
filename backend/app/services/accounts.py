from typing import List, Optional
from uuid import UUID

from app.repositories.accounts import InMemoryAccountRepository
from app.schemas.accounts import AccountCreate, AccountRead


class AccountService:
    def __init__(self, repository: InMemoryAccountRepository) -> None:
        self._repository = repository

    def create_account(self, account: AccountCreate) -> AccountRead:
        return self._repository.create(account)

    def get_account(self, account_id: UUID) -> Optional[AccountRead]:
        return self._repository.get(account_id)

    def list_accounts(self) -> List[AccountRead]:
        return self._repository.list()
