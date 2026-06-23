from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.accounts import AccountCreate, AccountRead


class InMemoryAccountRepository:
    def __init__(self) -> None:
        self._accounts: List[AccountRead] = []

    def create(self, account: AccountCreate) -> AccountRead:
        now = datetime.now(timezone.utc)
        account_read = AccountRead(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            current_balance_cents=account.opening_balance_cents,
            **account.model_dump(exclude={"opening_balance_cents"}),
        )
        self._accounts.append(account_read)
        return account_read

    def get(self, account_id: UUID) -> Optional[AccountRead]:
        return next(
            (account for account in self._accounts if account.id == account_id),
            None,
        )

    def list(self) -> List[AccountRead]:
        return list(self._accounts)
