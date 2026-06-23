from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_category_service
from app.schemas.categories import CategoryCreate, CategoryRead
from app.services.categories import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryRead, status_code=201)
def create_category(
    category: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(category)


@router.get("", response_model=List[CategoryRead])
def list_categories(
    service: CategoryService = Depends(get_category_service),
):
    return service.list_categories()


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category
