from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from app.schemas.categories import CategoryCreate, CategoryRead


class InMemoryCategoryRepository:
    def __init__(self) -> None:
        self._categories: List[CategoryRead] = []

    def create(self, category: CategoryCreate) -> CategoryRead:
        now = datetime.now(timezone.utc)
        category_read = CategoryRead(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **category.model_dump(),
        )
        self._categories.append(category_read)
        return category_read

    def get(self, category_id: UUID) -> Optional[CategoryRead]:
        return next(
            (category for category in self._categories if category.id == category_id),
            None,
        )

    def list(self) -> List[CategoryRead]:
        return list(self._categories)
