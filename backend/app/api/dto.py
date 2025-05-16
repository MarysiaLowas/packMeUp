from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LuggageModel(BaseModel):
    max_weight: Optional[float] = Field(
        None,
        gt=0,
        description="Maximum weight capacity in kg (optional)",
        alias="maxWeight",
    )
    dimensions: Optional[str] = Field(
        None, description="Dimensions in format WxHxD (e.g. '45x35x20')"
    )

    @model_validator(mode="after")
    def check_at_least_one_spec_provided(self) -> "LuggageModel":
        max_weight_val = self.max_weight
        dimensions_val = self.dimensions

        if max_weight_val is None and dimensions_val is None:
            raise ValueError(
                "At least one of max_weight or dimensions must be provided for each luggage item"
            )
        return self

    @field_validator("dimensions")
    @classmethod
    def validate_dimensions_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        parts = v.lower().replace(" ", "").split("x")
        if len(parts) != 3 or not all(p.replace(".", "").isdigit() for p in parts):
            raise ValueError(
                "Dimensions, if provided, must be in format WxHxD (e.g. '45x35x20')"
            )
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class GeneratedListItemDTO(BaseModel):
    id: UUID
    item_name: str = Field(..., alias="itemName")
    quantity: int
    is_packed: bool = Field(..., alias="isPacked")
    item_category: Optional[str] = Field(None, alias="itemCategory")
    item_weight: Optional[float] = Field(None, alias="itemWeight")
    item_dimensions: Optional[str] = Field(None, alias="itemDimensions")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class GeneratedListSummaryDTO(BaseModel):
    id: UUID
    name: str
    trip_id: UUID = Field(..., alias="tripId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    items_count: int = Field(..., alias="itemsCount")
    packed_items_count: int = Field(..., alias="packedItemsCount")

    @field_validator("items_count", "packed_items_count", mode="before")
    @classmethod
    def compute_counts(cls, v, values, **kwargs):
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class PaginatedGeneratedListResponse(BaseModel):
    items: List[GeneratedListSummaryDTO]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")
    total_pages: int = Field(..., alias="totalPages")

    model_config = ConfigDict(populate_by_name=True)


class GeneratePackingListResponseDTO(BaseModel):
    id: UUID
    name: str
    trip_id: UUID = Field(..., alias="tripId")
    items: List[GeneratedListItemDTO]
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    items_count: int = Field(..., alias="itemsCount")
    packed_items_count: int = Field(..., alias="packedItemsCount")

    @field_validator("items_count", "packed_items_count", mode="before")
    @classmethod
    def compute_counts(cls, v, values, **kwargs):
        if isinstance(values, dict) and "items" in values:
            items = values["items"]
            if v == "items_count":
                return len(items)
            elif v == "packed_items_count":
                return sum(1 for item in items if item.is_packed)
        return v

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
