from typing import Optional

from pydantic import Field

from .common import APIModel, AccountType, CurrencyCode, MoneyCents, TimestampedRead


class AccountBase(APIModel):
    name: str = Field(min_length=1, max_length=120)
    account_type: AccountType
    currency: CurrencyCode = CurrencyCode.USD
    institution_name: Optional[str] = Field(default=None, max_length=120)
    is_archived: bool = False


class AccountCreate(AccountBase):
    opening_balance_cents: MoneyCents = Field(
        default=0,
        description="Initial account balance in the smallest currency unit.",
    )


class AccountUpdate(APIModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    account_type: Optional[AccountType] = None
    institution_name: Optional[str] = Field(default=None, max_length=120)
    is_archived: Optional[bool] = None


class AccountRead(AccountBase, TimestampedRead):
    current_balance_cents: MoneyCents
