from typing import List

from fastapi import APIRouter, Depends

from app.repositories.transactions import InMemoryTransactionRepository
from app.schemas.transactions import TransactionCreate, TransactionRead
from app.services.transactions import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])

transaction_repository = InMemoryTransactionRepository()


def get_transaction_service() -> TransactionService:
    return TransactionService(transaction_repository)


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
