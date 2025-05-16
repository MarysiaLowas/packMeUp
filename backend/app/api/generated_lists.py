from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dto import GeneratePackingListResponseDTO
from app.models import GeneratedList, GeneratedListItem

router = APIRouter(prefix="/api/generated-lists", tags=["generated-lists"])


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
) -> GeneratePackingListResponseDTO:
    """Retrieve a generated packing list with all its items."""
    try:
        # Get the generated list with items
        query = (
            select(GeneratedList)
            .where(GeneratedList.id == list_id)
            .options(selectinload(GeneratedList.items))
        )
        result = await GeneratedList.select_one(query)

        if not result:
            raise HTTPException(status_code=404, detail="List not found")

        return GeneratePackingListResponseDTO.from_orm(result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get packing list") from e


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
    is_packed: bool = Body(..., embed=True),
) -> None:
    """Update a packing list item's packed status."""
    try:
        # Get the item and verify it belongs to the correct list
        item = await GeneratedListItem.get(id=item_id)
        if not item or item.generated_list_id != list_id:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update the item
        await item.update(is_packed=is_packed)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update item") from e
