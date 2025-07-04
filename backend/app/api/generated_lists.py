from math import ceil
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from fastapi_sqlalchemy import async_db as db
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.api.auth import get_current_user_id
from app.api.dto import (
    GeneratedListItemDTO,
    GeneratedListSummaryDTO,
    GeneratePackingListResponseDTO,
    PaginatedGeneratedListResponse,
)
from app.models import GeneratedList, GeneratedListItem

router = APIRouter(prefix="/api/generated-lists", tags=["generated-lists"])


class UpdateListItemDTO(BaseModel):
    is_packed: bool = Field(..., alias="isPacked")

    model_config = ConfigDict(populate_by_name=True)


@router.get(
    "/{list_id}",
    response_model=GeneratePackingListResponseDTO,
    summary="Get a generated packing list",
    responses={
        200: {"description": "Packing list retrieved successfully"},
        404: {"description": "List not found"},
    },
)
async def get_generated_list(
    list_id: UUID = Path(..., description="The ID of the generated list"),
    current_user_id: UUID = Depends(get_current_user_id),
) -> GeneratePackingListResponseDTO:
    """Retrieve a generated packing list with all its items."""
    try:
        # Get the generated list with items
        query = (
            select(GeneratedList)
            .where(GeneratedList.id == list_id)
            .where(GeneratedList.user_id == current_user_id)
            .options(selectinload(GeneratedList.items))
        )
        generated_list = await GeneratedList.select_one(query)

        if not generated_list:
            raise HTTPException(status_code=404, detail="List not found")

        # Count packed items
        packed_items = sum(1 for item in generated_list.items if item.is_packed)

        return GeneratePackingListResponseDTO(
            id=generated_list.id,
            name=generated_list.name,
            tripId=generated_list.trip_id,
            items=[
                GeneratedListItemDTO(
                    id=item.id,
                    itemName=item.item_name,
                    quantity=item.quantity,
                    isPacked=item.is_packed,
                    itemCategory=item.item_category,
                    itemWeight=item.item_weight,
                    itemDimensions=item.item_dimensions,
                    createdAt=item.created_at,
                    updatedAt=item.updated_at,
                )
                for item in generated_list.items
            ],
            createdAt=generated_list.created_at,
            updatedAt=generated_list.updated_at,
            itemsCount=len(generated_list.items),
            packedItemsCount=packed_items,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get packing list") from e


@router.get(
    "/",
    response_model=PaginatedGeneratedListResponse,
    summary="List user's packing lists",
    response_description="List of packing lists with pagination",
)
async def list_generated_lists(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    search: Optional[str] = None,
    trip_id: Optional[UUID] = None,
    sort_field: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    current_user_id: UUID = Depends(get_current_user_id),
) -> PaginatedGeneratedListResponse:
    """Get all packing lists for the current user with pagination, filtering, and sorting."""
    try:
        print(
            f"[DEBUG] Input parameters: page={page}, page_size={page_size}, search={search}, "
            f"trip_id={trip_id}, sort_field={sort_field}, sort_order={sort_order}, "
            f"current_user_id={current_user_id}"
        )

        # Get all lists for the user
        query = (
            select(GeneratedList)
            .where(GeneratedList.user_id == current_user_id)
            .options(selectinload(GeneratedList.items))
        )
        lists = (await db.session.execute(query)).scalars().all()

        # Filter lists
        filtered_lists = lists
        if search:
            filtered_lists = [
                lst for lst in filtered_lists if search.lower() in lst.name.lower()
            ]
        if trip_id:
            filtered_lists = [lst for lst in filtered_lists if lst.trip_id == trip_id]

        # Sort lists
        if sort_field == "name":
            filtered_lists = sorted(
                filtered_lists,
                key=lambda x: x.name,
                reverse=sort_order.lower() == "desc",
            )
        elif sort_field == "trip_id":
            filtered_lists = sorted(
                filtered_lists,
                key=lambda x: x.trip_id,
                reverse=sort_order.lower() == "desc",
            )
        else:  # default to created_at
            filtered_lists = sorted(
                filtered_lists,
                key=lambda x: x.created_at,
                reverse=sort_order.lower() == "desc",
            )

        # Calculate total and pages
        total = len(filtered_lists)
        total_pages = ceil(total / page_size) if total > 0 else 0

        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        paginated_lists = filtered_lists[start:end]

        # Prepare items with computed fields
        items = []
        for lst in paginated_lists:
            packed_items = sum(1 for item in lst.items if item.is_packed)
            items.append(
                GeneratedListSummaryDTO(
                    id=lst.id,
                    name=lst.name,
                    tripId=lst.trip_id,
                    createdAt=lst.created_at,
                    updatedAt=lst.updated_at,
                    itemsCount=len(lst.items),
                    packedItemsCount=packed_items,
                )
            )

        # Prepare the response
        return PaginatedGeneratedListResponse(
            items=items,
            total=total,
            page=page,
            pageSize=page_size,
            totalPages=total_pages,
        )

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get packing lists",
        )


@router.patch(
    "/{list_id}/items/{item_id}",
    status_code=200,
    summary="Update a packing list item",
    responses={
        200: {"description": "Item updated successfully"},
        404: {"description": "Item not found"},
    },
)
async def update_list_item(
    list_id: UUID = Path(..., description="The ID of the generated list"),
    item_id: UUID = Path(..., description="The ID of the item to update"),
    update_data: UpdateListItemDTO = Body(...),
) -> None:
    """Update a packing list item's packed status."""
    try:
        # Get the item and verify it belongs to the correct list
        query = (
            select(GeneratedListItem)
            .where(GeneratedListItem.id == item_id)
            .where(GeneratedListItem.generated_list_id == list_id)
        )
        item = await GeneratedListItem.select_one(query)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update the item using SQLAlchemy update
        update_stmt = (
            update(GeneratedListItem)
            .where(GeneratedListItem.id == item_id)
            .values(is_packed=update_data.is_packed)
        )
        await db.session.execute(update_stmt)
        await db.session.commit()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[DEBUG] Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item") from e
