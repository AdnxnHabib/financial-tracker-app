from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_account_service
from app.schemas.accounts import AccountCreate, AccountRead
from app.services.accounts import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("", response_model=AccountRead, status_code=201)
def create_account(
    account: AccountCreate,
    service: AccountService = Depends(get_account_service),
):
    return service.create_account(account)


@router.get("", response_model=List[AccountRead])
def list_accounts(
    service: AccountService = Depends(get_account_service),
):
    return service.list_accounts()


@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    account_id: UUID,
    service: AccountService = Depends(get_account_service),
):
    account = service.get_account(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    return account
