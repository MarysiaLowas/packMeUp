from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


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


class GeneratePackingListResponseDTO(BaseModel):
    id: UUID
    name: str
    items: List[GeneratedListItemDTO]
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
