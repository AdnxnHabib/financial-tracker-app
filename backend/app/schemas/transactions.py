from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import Field, model_validator

from .common import (
    APIModel,
    CurrencyCode,
    MoneyCents,
    PaymentMethod,
    TimestampedRead,
    TransactionStatus,
    TransactionType,
)


class TransactionBase(APIModel):
    account_id: UUID
    category_id: Optional[UUID] = None
    transaction_type: TransactionType
    amount_cents: MoneyCents = Field(
        ge=1,
        description="Absolute amount in the smallest currency unit.",
    )
    currency: CurrencyCode = CurrencyCode.USD
    transaction_date: date
    merchant_name: Optional[str] = Field(default=None, max_length=160)
    description: Optional[str] = Field(default=None, max_length=240)
    payment_method: PaymentMethod = PaymentMethod.OTHER
    status: TransactionStatus = TransactionStatus.CLEARED

    @model_validator(mode="after")
    def require_category_for_expenses(self):
        if self.transaction_type == TransactionType.EXPENSE and self.category_id is None:
            raise ValueError("Expense transactions require a category_id.")
        return self


class TransactionCreate(TransactionBase):
    external_id: Optional[str] = Field(
        default=None,
        max_length=160,
        description="Provider or import identifier used later for deduplication.",
    )


class TransactionUpdate(APIModel):
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    transaction_type: Optional[TransactionType] = None
    amount_cents: Optional[MoneyCents] = Field(default=None, ge=1)
    transaction_date: Optional[date] = None
    merchant_name: Optional[str] = Field(default=None, max_length=160)
    description: Optional[str] = Field(default=None, max_length=240)
    payment_method: Optional[PaymentMethod] = None
    status: Optional[TransactionStatus] = None


class TransactionRead(TransactionBase, TimestampedRead):
    external_id: Optional[str] = None
