from datetime import datetime
from typing import List, Optional, Literal, Annotated
from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class TagDTO(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


class ItemDTO(BaseModel):
    id: UUID
    name: str
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True


class SpecialListItemWithDetailsDTO(BaseModel):
    itemId: UUID
    quantity: int
    item: ItemDTO

    class Config:
        from_attributes = True


class SpecialListDTO(BaseModel):
    id: UUID
    userId: UUID
    name: str
    category: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class SpecialListDetailDTO(SpecialListDTO):
    items: List[SpecialListItemWithDetailsDTO]
    tags: List[TagDTO]

    class Config:
        from_attributes = True


class CreateSpecialListCommand(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    category: str


class UpdateSpecialListCommand(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    category: str


class AddSpecialListItemCommand(BaseModel):
    itemId: Optional[UUID] = None
    name: Annotated[str, Field(min_length=1, max_length=255)]
    quantity: int = Field(gt=0)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = None
    category: Optional[str] = None


class UpdateSpecialListItemCommand(BaseModel):
    quantity: int = Field(gt=0, description="The new quantity of the item")


class SpecialListFilter(BaseModel):
    category: Optional[str] = None
    search: Optional[str] = None


class PaginatedSpecialListResponse(BaseModel):
    items: List[SpecialListDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


class AddTagCommand(BaseModel):
    """Command for adding a tag to a special list."""

    tagId: Optional[UUID] = None
    name: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None

    @property
    def has_valid_input(self) -> bool:
        """Check if either tagId or name is provided."""
        return bool(self.tagId is not None or self.name)


class SortField(str, Enum):
    """Valid fields for sorting special lists."""

    NAME = "name"
    CATEGORY = "category"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SortOrder(str, Enum):
    """Valid sort orders."""

    ASC = "asc"
    DESC = "desc"


class SpecialListSort(BaseModel):
    """Sorting options for special lists."""

    field: Literal[
        SortField.NAME, SortField.CATEGORY, SortField.CREATED_AT, SortField.UPDATED_AT
    ] = SortField.CREATED_AT
    order: Literal[SortOrder.ASC, SortOrder.DESC] = SortOrder.DESC
