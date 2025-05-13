from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Path, status, Body
from pydantic import BaseModel, Field, field_validator, root_validator

from app.models import Trip
from app.services.constants import (
    AccommodationType, TransportType, SeasonType,
    CateringType, CATERING_OPTIONS
)
from app.services.trip_service import TripService
from app.api.dto import (
    LuggageModel, GeneratedListItemDTO,
    GeneratePackingListResponseDTO
)

router = APIRouter(prefix="/api/trips", tags=["trips"])

class LuggageModel(BaseModel):
    max_weight: Optional[float] = Field(None, gt=0, description="Maximum weight capacity in kg (optional)", alias="maxWeight")
    dimensions: Optional[str] = Field(None, description="Dimensions in format WxHxD (e.g. '45x35x20') (optional)", alias="dimensions")

    @root_validator(pre=False, skip_on_failure=True)
    @classmethod
    def check_at_least_one_spec_provided(cls, values):
        max_weight_val = values.get('max_weight')
        dimensions_val = values.get('dimensions')
        
        if max_weight_val is None and dimensions_val is None:
            raise ValueError("At least one of max_weight or dimensions must be provided for each luggage item")
        return values

    @field_validator("dimensions")
    @classmethod
    def validate_dimensions_format(cls, v):
        if v is None:
            return v
        parts = v.lower().replace(" ", "").split("x")
        if len(parts) != 3 or not all(p.replace(".", "").isdigit() for p in parts):
            raise ValueError("Dimensions, if provided, must be in format WxHxD (e.g. '45x35x20')")
        return v

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

class CreateTripCommand(BaseModel):
    destination: str = Field(..., min_length=3, description="Trip destination")
    start_date: Optional[date] = Field(None, description="Trip start date", alias="startDate")
    duration_days: int = Field(..., gt=0, description="Trip duration in days", alias="durationDays")
    num_adults: int = Field(..., ge=1, description="Number of adults", alias="numAdults")
    children_ages: Optional[List[int]] = Field(None, description="List of children ages", alias="childrenAges")
    accommodation: Optional[AccommodationType] = Field(None, description="Type of accommodation")
    catering: Optional[List[int]] = Field(None, description="List of catering options")
    transport: Optional[TransportType] = Field(None, description="Type of transport")
    activities: Optional[List[str]] = Field(None, description="List of planned activities")
    season: Optional[SeasonType] = Field(None, description="Season of the trip")
    available_luggage: Optional[List[LuggageModel]] = Field(None, description="Available luggage details", alias="availableLuggage")

    @field_validator("children_ages")
    @classmethod
    def validate_children_ages(cls, v):
        if v is not None:
            if not all(isinstance(age, int) and age >= 0 for age in v):
                raise ValueError("All children ages must be non-negative integers")
        return v

    @field_validator("catering")
    @classmethod
    def validate_catering(cls, v):
        if v is not None:
            valid_options = [opt[0] for opt in CATERING_OPTIONS]
            invalid_options = [opt for opt in v if opt not in valid_options]
            if invalid_options:
                raise ValueError(
                    f"Invalid catering options: {invalid_options}. "
                    f"Valid options are: {dict(CATERING_OPTIONS)}"
                )
        return v

    class Config:
        allow_population_by_field_name = True

class TripDTO(BaseModel):
    id: UUID
    user_id: UUID
    destination: str
    start_date: Optional[date]
    duration_days: int
    num_adults: int
    children_ages: Optional[List[int]]
    accommodation: Optional[AccommodationType]
    catering: Optional[List[int]]
    transport: Optional[TransportType]
    activities: Optional[List[str]]
    season: Optional[SeasonType]
    available_luggage: Optional[List[LuggageModel]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ListTripsResponseDTO(BaseModel):
    trips: List[TripDTO]
    total: int
    
    class Config:
        from_attributes = True

class GeneratePackingListCommand(BaseModel):
    """Optional command for customizing packing list generation."""
    include_special_lists: Optional[List[UUID]] = Field(None, description="IDs of special lists to include in generation", alias="includeSpecialLists")
    exclude_categories: Optional[List[str]] = Field(None, description="Categories to exclude from generation", alias="excludeCategories")
    
    class Config:
        allow_population_by_field_name = True

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
    
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class GeneratePackingListResponseDTO(BaseModel):
    id: UUID
    name: str
    items: List[GeneratedListItemDTO]
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

@router.post(
    "",
    response_model=TripDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new trip",
    response_description="Created trip details",
    responses={
        201: {
            "description": "Trip created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "user_id": "123e4567-e89b-12d3-a456-426614174001",
                        "destination": "Paris, France",
                        "start_date": "2024-06-15",
                        "end_date": "2024-06-25",
                        "duration_days": 10,
                        "num_adults": 2,
                        "children_ages": [5, 8],
                        "accommodation": "hotel",
                        "catering": [0],
                        "transport": "plane",
                        "activities": ["sightseeing", "museums"],
                        "season": "summer",
                        "available_luggage": [
                            {
                                "max_weight": 23.0,
                                "dimensions": "55x40x20"
                            }
                        ],
                        "created_at": "2024-03-15T10:30:00Z",
                        "updated_at": "2024-03-15T10:30:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "End date must be after start date"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to create trip"
                    }
                }
            }
        }
    }
)
async def create_trip(
    command: CreateTripCommand,
) -> Trip:
    """
    Create a new trip with the provided details.
    
    The endpoint accepts trip configuration including:
    - Basic trip info (destination, dates, duration)
    - Party composition (adults, children)
    - Travel preferences (accommodation, transport)
    - Available luggage details
    
    All dates are in ISO format (YYYY-MM-DD).
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        trip_data = {
            "accommodation": command.accommodation.value if command.accommodation else None,
            "transport": command.transport.value if command.transport else None,
            "season": command.season.value if command.season else None,
            "num_adults": command.num_adults,
            "children_ages": command.children_ages,
            "catering": command.catering,
            "activities": command.activities,
            "available_luggage": [item.dict() for item in command.available_luggage] if command.available_luggage else None
        }
        
        return await TripService.create_trip(
            user_id=mock_user_id,
            destination=command.destination,
            duration_days=command.duration_days,
            start_date=command.start_date,
            **trip_data
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create trip"
        ) from e 

@router.get(
    "/",
    response_model=ListTripsResponseDTO,
    summary="List user's trips",
    response_description="List of trips with pagination",
    responses={
        200: {
            "description": "List of trips retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "trips": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174000",
                                "destination": "Paris, France",
                                "start_date": "2024-06-15",
                                "duration_days": 10,
                                "created_at": "2024-03-15T10:30:00Z"
                            }
                        ],
                        "total": 1
                    }
                }
            }
        },
        400: {
            "description": "Invalid query parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid sort field. Allowed fields are: created_at, destination, start_date, duration_days"
                    }
                }
            }
        }
    }
)
async def list_trips(
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of trips to return (1-100)",
        example=10
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of trips to skip for pagination",
        example=0
    ),
    sort: Optional[str] = Query(
        None,
        description="Sort field (created_at, destination, start_date, duration_days)",
        example="created_at"
    )
) -> ListTripsResponseDTO:
    """
    List trips for the current user with pagination and sorting options.
    
    The endpoint supports:
    - Pagination with limit and offset
    - Sorting by various fields
    - Default sorting by creation date (descending)
    
    Sort fields:
    - created_at: Sort by creation date
    - destination: Sort alphabetically by destination
    - start_date: Sort by trip start date
    - duration_days: Sort by trip duration
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        trips, total = await TripService.list_trips(
            user_id=mock_user_id,
            limit=limit,
            offset=offset,
            sort=sort
        )
        return ListTripsResponseDTO(trips=trips, total=total)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to list trips"
        ) from e 

@router.get(
    "/{trip_id}",
    response_model=TripDTO,
    summary="Get trip details",
    response_description="Detailed trip information",
    responses={
        200: {
            "description": "Trip details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "destination": "Paris, France",
                        "start_date": "2024-06-15",
                        "end_date": "2024-06-25",
                        "duration_days": 10,
                        "accommodation": "hotel",
                        "created_at": "2024-03-15T10:30:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Trip not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Trip not found"
                    }
                }
            }
        }
    }
)
async def get_trip(
    trip_id: UUID = Path(..., description="The ID of the trip to retrieve", example="123e4567-e89b-12d3-a456-426614174000")
) -> Trip:
    """
    Retrieve detailed information about a specific trip.
    
    The endpoint returns full trip details including:
    - Basic trip information
    - Party composition
    - Travel preferences
    - Luggage details
    - Creation and update timestamps
    
    If the trip doesn't exist or belongs to another user, a 404 error is returned.
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        trip = await TripService.get_trip(trip_id, user_id=mock_user_id)
        if not trip:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
        return trip
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to get trip"
        ) from e 

@router.post(
    "/{trip_id}/generate-list",
    response_model=GeneratePackingListResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a packing list for a trip",
    response_description="Generated packing list details",
    responses={
        201: {
            "description": "Packing list generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Packing List for Paris Trip",
                        "items": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174001",
                                "itemName": "Toothbrush",
                                "quantity": 1,
                                "isPacked": False,
                                "itemCategory": "Hygiene"
                            }
                        ],
                        "createdAt": "2024-03-15T10:30:00Z"
                    }
                }
            }
        },
        404: {
            "description": "Trip not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Trip not found"
                    }
                }
            }
        },
        403: {
            "description": "Access denied",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Access denied"
                    }
                }
            }
        }
    }
)
async def generate_packing_list(
    trip_id: UUID = Path(..., description="The ID of the trip to generate a packing list for"),
    command: Optional[GeneratePackingListCommand] = None,
) -> GeneratePackingListResponseDTO:
    """
    Generate a packing list for a specific trip using AI.
    
    The endpoint:
    - Validates trip existence and user ownership
    - Uses trip details to generate a personalized packing list
    - Optionally includes items from user's special lists
    - Creates a new generated list with items
    
    The generation process considers:
    - Trip duration and destination
    - Number of travelers and their ages
    - Planned activities and accommodation type
    - Available luggage specifications
    - Season and transport mode
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        # Validate trip exists and belongs to user
        trip = await TripService.get_trip(trip_id, user_id=mock_user_id)
        if not trip:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
            
        # Generate packing list using AI service
        return await TripService.generate_packing_list(
            trip=trip,
            user_id=mock_user_id,
            include_special_lists=command.include_special_lists if command else None,
            exclude_categories=command.exclude_categories if command else None
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate packing list: {str(e)}"
        ) from e

@router.get(
    "/{trip_id}/lists/{list_id}",
    response_model=GeneratePackingListResponseDTO,
    summary="Get a generated packing list",
    response_description="Generated packing list details",
    responses={
        200: {
            "description": "Packing list retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Packing List for Paris Trip",
                        "items": [
                            {
                                "id": "123e4567-e89b-12d3-a456-426614174001",
                                "itemName": "Toothbrush",
                                "quantity": 1,
                                "isPacked": False,
                                "itemCategory": "Hygiene"
                            }
                        ],
                        "createdAt": "2024-03-15T10:30:00Z"
                    }
                }
            }
        },
        404: {
            "description": "List not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "List not found"
                    }
                }
            }
        }
    }
)
async def get_generated_list(
    trip_id: UUID = Path(..., description="The ID of the trip"),
    list_id: UUID = Path(..., description="The ID of the generated list")
) -> GeneratePackingListResponseDTO:
    """
    Retrieve a generated packing list with all its items.
    
    The endpoint returns:
    - List details (name, creation date)
    - All items with their details and packed status
    - Items are grouped by category
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        # Get the trip first to verify ownership
        trip = await TripService.get_trip(trip_id, user_id=mock_user_id)
        if not trip:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
        
        # Get the generated list with items
        query = (
            select(GeneratedList)
            .where(GeneratedList.id == list_id)
            .where(GeneratedList.trip_id == trip_id)
            .options(selectinload(GeneratedList.items))
        )
        result = await GeneratedList.select_one(query)
        if not result:
            raise HTTPException(
                status_code=404,
                detail="List not found"
            )
            
        return GeneratePackingListResponseDTO.from_orm(result)
            
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to get packing list"
        ) from e

class UpdateListItemCommand(BaseModel):
    is_packed: bool = Field(..., alias="isPacked")

    class Config:
        allow_population_by_field_name = True

@router.patch(
    "/{trip_id}/lists/{list_id}/items/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Update a packing list item",
    response_description="Item updated successfully",
    responses={
        200: {
            "description": "Item updated successfully"
        },
        404: {
            "description": "Item not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Item not found"
                    }
                }
            }
        }
    }
)
async def update_list_item(
    trip_id: UUID = Path(..., description="The ID of the trip"),
    list_id: UUID = Path(..., description="The ID of the generated list"),
    item_id: UUID = Path(..., description="The ID of the item to update"),
    command: UpdateListItemCommand = Body(..., description="Update command")
) -> None:
    """
    Update a packing list item's status.
    
    Currently supports:
    - Marking items as packed/unpacked
    """
    # TODO: Add proper authentication and user handling
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        # Get the trip first to verify ownership
        trip = await TripService.get_trip(trip_id, user_id=mock_user_id)
        if not trip:
            raise HTTPException(
                status_code=404,
                detail="Trip not found"
            )
        
        # Get the item and verify it belongs to the correct list
        item = await GeneratedListItem.get(id=item_id)
        if not item or item.generated_list_id != list_id:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )
            
        # Update the item
        await item.update(is_packed=command.is_packed)
            
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to update item"
        ) from e
