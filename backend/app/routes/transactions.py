from typing import List

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_transaction_service
from app.schemas.transactions import (
    RecentTransactionRead,
    TransactionCreate,
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


@router.get("", response_model=List[TransactionRead])
def list_transactions(
    service: TransactionService = Depends(get_transaction_service),
):
    return service.list_transactions()


@router.get("/recent", response_model=List[RecentTransactionRead])
def list_recent_transactions(
    limit: int = Query(default=5, ge=1, le=50),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.list_recent_transactions(limit=limit)
