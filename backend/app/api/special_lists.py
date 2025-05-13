from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import math

from app.models import User, SpecialList, SpecialListItem, Item, Tag
from app.schemas.special_lists import (
    CreateSpecialListCommand,
    SpecialListDTO,
    SpecialListDetailDTO,
    UpdateSpecialListCommand,
    AddSpecialListItemCommand,
    SpecialListItemWithDetailsDTO,
    UpdateSpecialListItemCommand,
    SpecialListFilter,
    PaginatedSpecialListResponse,
    AddTagCommand,
    TagDTO,
    SortField,
    SortOrder,
    SpecialListSort
)
from app.services.special_list_service import SpecialListService, SpecialListError

router = APIRouter(
    prefix="/api/special-lists",
    tags=["special-lists"],
)

class SpecialListError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

@router.post("", response_model=SpecialListDTO, status_code=status.HTTP_201_CREATED, summary="Create a new special list", response_description="Created special list details")
async def create_special_list(
    data: CreateSpecialListCommand
) -> SpecialListDTO:
    """Create a new special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        return await SpecialListService.create_special_list(user_id=mock_user_id, data=data)
    except SpecialListError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create special list"
        ) from e

@router.get("/", response_model=PaginatedSpecialListResponse)
async def get_special_lists(
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_field: SortField = Query(SortField.CREATED_AT, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="Sort order")
) -> PaginatedSpecialListResponse:
    """Get all special lists for the current user with pagination, filtering, and sorting."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        filters = SpecialListFilter(category=category, search=search) if (category or search) else None
        sort = SpecialListSort(field=sort_field, order=sort_order)
        lists, total = await SpecialListService.get_user_lists(user_id=mock_user_id, page=page, page_size=page_size, filters=filters, sort=sort)
        total_pages = math.ceil(total / page_size)
        return PaginatedSpecialListResponse(
            items=[SpecialListDTO.from_orm(lst) for lst in lists],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get special lists"
        )

@router.get("/{list_id}", response_model=SpecialListDetailDTO)
async def get_special_list(
    list_id: UUID
) -> SpecialListDetailDTO:
    """Get a special list with all its items and tags."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        special_list = await SpecialListService.get_list_with_details(list_id, user_id=mock_user_id)
        return SpecialListDetailDTO.from_orm(special_list)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get special list details")

@router.put("/{list_id}", response_model=SpecialListDTO)
async def update_special_list(
    list_id: UUID,
    data: UpdateSpecialListCommand
) -> SpecialListDTO:
    """Update a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        special_list = await SpecialListService.update_special_list(list_id, user_id=mock_user_id, data=data)
        return SpecialListDTO.from_orm(special_list)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update special list")

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_special_list(
    list_id: UUID
) -> None:
    """Delete a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        await SpecialListService.delete_special_list(list_id, user_id=mock_user_id)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete special list")

@router.post("/{list_id}/items", response_model=SpecialListItemWithDetailsDTO)
async def add_item_to_list(
    list_id: UUID,
    data: AddSpecialListItemCommand
) -> SpecialListItemWithDetailsDTO:
    """Add an item to a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        special_list_item = await SpecialListService.add_item_to_list(list_id, user_id=mock_user_id, data=data)
        return SpecialListItemWithDetailsDTO(
            itemId=special_list_item.item_id,
            quantity=special_list_item.quantity,
            item=special_list_item.item
        )
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add item to special list")

@router.delete("/{list_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_list(
    list_id: UUID,
    item_id: UUID
) -> None:
    """Remove an item from a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        await SpecialListService.remove_item_from_list(list_id, item_id, user_id=mock_user_id)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove item from special list")

@router.put("/{list_id}/items/{item_id}", response_model=SpecialListItemWithDetailsDTO)
async def update_list_item_quantity(
    list_id: UUID,
    item_id: UUID,
    data: UpdateSpecialListItemCommand
) -> SpecialListItemWithDetailsDTO:
    """Update the quantity of an item in a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        special_list_item = await SpecialListService.update_list_item_quantity(list_id, item_id, user_id=mock_user_id, data=data)
        return SpecialListItemWithDetailsDTO(
            itemId=special_list_item.item_id,
            quantity=special_list_item.quantity,
            item=special_list_item.item
        )
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update special list item")

@router.post("/{list_id}/tags", response_model=TagDTO)
async def add_tag_to_list(
    list_id: UUID,
    data: AddTagCommand
) -> TagDTO:
    """Add a tag to a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        tag = await SpecialListService.add_tag_to_list(list_id, user_id=mock_user_id, data=data)
        return TagDTO.from_orm(tag)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add tag to special list")

@router.delete("/{list_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag_from_list(
    list_id: UUID,
    tag_id: UUID
) -> None:
    """Remove a tag from a special list."""
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    try:
        await SpecialListService.remove_tag_from_list(list_id, tag_id, user_id=mock_user_id)
    except SpecialListError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove tag from special list") 
