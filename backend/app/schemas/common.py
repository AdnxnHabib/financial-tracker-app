from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        str_strip_whitespace=True,
    )


class TimestampedRead(APIModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CurrencyCode(str, Enum):
    USD = "USD"
    CAD = "CAD"


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    CASH = "cash"
    INVESTMENT = "investment"
    LOAN = "loan"
    OTHER = "other"


class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    CLEARED = "cleared"
    EXCLUDED = "excluded"


class PaymentMethod(str, Enum):
    CARD = "card"
    CASH = "cash"
    ACH = "ach"
    WIRE = "wire"
    CHECK = "check"
    OTHER = "other"


MoneyCents = int


def money_field(description: str, *, allow_zero: bool = False):
    lower_bound = 0 if allow_zero else 1
    return Field(ge=lower_bound, description=description)


OptionalName = Optional[str]
