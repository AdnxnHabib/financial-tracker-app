from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_transaction_service
from app.schemas.transactions import (
    TransactionCreate,
    TransactionFilters,
    TransactionListRead,
    TransactionRead,
)
from app.services.transactions import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionRead, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service),
):
    return service.create_transaction(transaction)


@router.get("", response_model=List[TransactionListRead])
def list_transactions(
    filters: TransactionFilters = Depends(),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.list_transactions(filters)
