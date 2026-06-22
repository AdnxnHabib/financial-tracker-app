from typing import Optional

from pydantic import Field

from .common import APIModel, TimestampedRead


class CategoryBase(APIModel):
    name: str = Field(min_length=1, max_length=80)
    color: str = Field(
        default="#4f5cf6",
        pattern=r"^#[0-9a-fA-F]{6}$",
        description="Hex color used by charts and category labels.",
    )
    icon: Optional[str] = Field(default=None, max_length=40)
    is_archived: bool = False


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(APIModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon: Optional[str] = Field(default=None, max_length=40)
    is_archived: Optional[bool] = None


class CategoryRead(CategoryBase, TimestampedRead):
    pass
