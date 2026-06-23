from typing import List, Optional
from uuid import UUID

from app.repositories.categories import InMemoryCategoryRepository
from app.schemas.categories import CategoryCreate, CategoryRead


class CategoryService:
    def __init__(self, repository: InMemoryCategoryRepository) -> None:
        self._repository = repository

    def create_category(self, category: CategoryCreate) -> CategoryRead:
        return self._repository.create(category)

    def get_category(self, category_id: UUID) -> Optional[CategoryRead]:
        return self._repository.get(category_id)

    def list_categories(self) -> List[CategoryRead]:
        return self._repository.list()
