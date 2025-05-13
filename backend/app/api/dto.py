from datetime import date, datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.services.constants import AccommodationType, TransportType, SeasonType

class LuggageModel(BaseModel):
    max_weight: Optional[float] = Field(None, gt=0, description="Maximum weight capacity in kg (optional)")
    dimensions: Optional[str] = Field(None, description="Dimensions in format WxHxD (e.g. '45x35x20')")

    @computed_field
    @property
    def maxWeight(self) -> Optional[float]:
        return self.max_weight

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class GeneratedListItemDTO(BaseModel):
    id: UUID
    item_name: str
    quantity: int
    is_packed: bool
    item_category: Optional[str] = None
    item_weight: Optional[float] = None
    item_dimensions: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    @computed_field
    @property
    def itemName(self) -> str:
        return self.item_name

    @computed_field
    @property
    def isPacked(self) -> bool:
        return self.is_packed

    @computed_field
    @property
    def itemCategory(self) -> Optional[str]:
        return self.item_category

    @computed_field
    @property
    def itemWeight(self) -> Optional[float]:
        return self.item_weight

    @computed_field
    @property
    def itemDimensions(self) -> Optional[str]:
        return self.item_dimensions

    @computed_field
    @property
    def createdAt(self) -> datetime:
        return self.created_at

    @computed_field
    @property
    def updatedAt(self) -> Optional[datetime]:
        return self.updated_at

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class GeneratePackingListResponseDTO(BaseModel):
    id: UUID
    name: str
    items: List[GeneratedListItemDTO]
    created_at: datetime
    updated_at: Optional[datetime] = None

    @computed_field
    @property
    def createdAt(self) -> datetime:
        return self.created_at

    @computed_field
    @property
    def updatedAt(self) -> Optional[datetime]:
        return self.updated_at

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    ) 