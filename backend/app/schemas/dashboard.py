from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .common import APIModel, CurrencyCode, MoneyCents, PaymentMethod


class MonthlyExpenseRead(APIModel):
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
    spent_cents: MoneyCents = Field(ge=0)
    budget_cents: Optional[MoneyCents] = Field(default=None, ge=0)
    currency: CurrencyCode


class CategorySpendRead(APIModel):
    category_id: UUID
    category_name: str
    color: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    spent_cents: MoneyCents = Field(ge=0)
    percent_of_total: float = Field(ge=0, le=100)
    currency: CurrencyCode


class RecentExpenseRead(APIModel):
    id: UUID
    merchant_name: Optional[str]
    category_name: str
    account_name: str
    amount_cents: MoneyCents = Field(ge=1)
    currency: CurrencyCode
    transaction_date: date
    payment_method: PaymentMethod


class DashboardRead(APIModel):
    monthly_expenses: List[MonthlyExpenseRead]
    top_categories: List[CategorySpendRead]
    recent_expenses: List[RecentExpenseRead]
