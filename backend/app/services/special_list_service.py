from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, or_, desc, asc
import math

from app.models import SpecialList, User, Item, Tag, SpecialListItem
from app.schemas.special_lists import (
    CreateSpecialListCommand,
    UpdateSpecialListCommand,
    AddSpecialListItemCommand,
    UpdateSpecialListItemCommand,
    SpecialListFilter,
    AddTagCommand,
    SpecialListSort,
    SortField,
    SortOrder
)

class SpecialListError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class SpecialListService:
    """Service for managing special lists."""
    
    @staticmethod
    async def get_lists(
        list_ids: List[UUID],
        user_id: UUID
    ) -> List[SpecialList]:
        """
        Get multiple special lists by their IDs, verifying user ownership.
        
        Args:
            list_ids: List of special list IDs to retrieve
            user_id: ID of the user who should own the lists
            
        Returns:
            List of found special lists with their items
            
        Note:
            Only returns lists that exist AND belong to the user.
            If a list doesn't exist or belongs to another user, it's silently skipped.
        """
        try:
            # Build query to get lists with their items
            query = (
                select(SpecialList)
                .where(
                    SpecialList.id.in_(list_ids),
                    SpecialList.user_id == user_id
                )
                .options(
                    selectinload(SpecialList.item_associations).selectinload(SpecialListItem.item)
                )
            )
            
            # Execute query using standard select
            results = await SpecialList.select(id=list_ids[0])  # Get first list
            if not results:
                return []
                
            special_lists = []
            for list_id in list_ids:
                list_result = await SpecialList.select(id=list_id)
                if list_result and list_result[0].user_id == user_id:
                    special_lists.append(list_result[0])
            
            return special_lists
            
        except Exception as e:
            print(f"Error fetching special lists: {e}")
            return []
    
    @staticmethod
    async def get_list(
        list_id: UUID,
        user_id: UUID
    ) -> Optional[SpecialList]:
        """
        Get a single special list by ID, verifying user ownership.
        
        Args:
            list_id: ID of the special list to retrieve
            user_id: ID of the user who should own the list
            
        Returns:
            SpecialList if found and owned by user, None otherwise
        """
        special_list = await SpecialList.get(
            id=list_id,
            include_items=True
        )
        
        # Verify ownership
        if special_list and special_list.user_id != user_id:
            return None
            
        return special_list

    @staticmethod
    async def create_special_list(user_id: UUID, data: CreateSpecialListCommand) -> SpecialList:
        # Check user's list limit using CrudMixin's select method
        lists_all = await SpecialList.select(user_id=user_id)
        if len(lists_all) >= 50:
            raise SpecialListError("User has reached maximum number of special lists", status_code=400)

        special_list_data = {
            "user_id": user_id,
            "name": data.name,
            "category": data.category
        }

        try:
            # Create new special list using CrudMixin's create method
            created_record = await SpecialList.create(**special_list_data)
            # Assuming the first element is the id
            created_id = created_record[0]
            # Re-query the created special list using CrudMixin's select method
            retrieved_list = await SpecialList.select(id=created_id)
            if not retrieved_list:
                raise SpecialListError("Failed to retrieve the created special list", status_code=500)
            result = retrieved_list[0]
            if isinstance(result, tuple):
                result = SpecialList(
                    id=result[0],
                    user_id=result[1],
                    name=result[2],
                    category=result[3],
                    created_at=result[4],
                    updated_at=result[5]
                )
            return result
        except IntegrityError as e:
            raise SpecialListError("Failed to create special list due to database constraint", status_code=400) from e
        except Exception as e:
            raise SpecialListError(f"Failed to create special list: {str(e)}", status_code=500) from e

    @staticmethod
    async def get_user_lists(
        user_id: UUID,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[SpecialListFilter] = None,
        sort: Optional[SpecialListSort] = None
    ) -> Tuple[List[SpecialList], int]:
        """Get all special lists for a user with pagination, filtering, and sorting.
        
        Args:
            user_id: The ID of the user
            page: The page number (1-based)
            page_size: The number of items per page
            filters: Optional filters to apply
            sort: Optional sorting options
            
        Returns:
            Tuple of (list of special lists, total count)
        """
        # Build equality filters using CrudMixin capabilities
        filter_kwargs = {"user_id": user_id}
        if filters and filters.category:
            filter_kwargs["category"] = filters.category

        # Retrieve all matching records based on equality filters
        lists_all = await SpecialList.select(**filter_kwargs)

        # If a search filter is provided, filter in Python
        if filters and filters.search:
            search_term = filters.search.lower()
            lists_all = [lst for lst in lists_all if search_term in lst.name.lower()]

        # Apply sorting
        if sort:
            lists_all = sorted(lists_all, key=lambda x: getattr(x, sort.field), reverse=(sort.order == SortOrder.DESC))
        else:
            lists_all = sorted(lists_all, key=lambda x: getattr(x, 'created_at'), reverse=True)

        total = len(lists_all)

        # Apply pagination slicing
        start = (page - 1) * page_size
        end = start + page_size
        paginated = lists_all[start:end]

        return paginated, total

    @staticmethod
    async def get_list_with_details(list_id: UUID, user_id: UUID) -> SpecialList:
        try:
            records = await SpecialList.select(id=list_id)
            if not records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)
            return special_list
        except Exception as e:
            raise SpecialListError(f"Failed to get special list details: {str(e)}", status_code=500) from e

    @staticmethod
    async def update_special_list(list_id: UUID, user_id: UUID, data: UpdateSpecialListCommand) -> SpecialList:
        try:
            records = await SpecialList.select(id=list_id)
            if not records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)
            special_list.name = data.name
            special_list.category = data.category
            # Assume special_list.save() commits the changes asynchronously
            await special_list.save()
            updated_records = await SpecialList.select(id=list_id)
            return updated_records[0]
        except IntegrityError as e:
            raise SpecialListError("Failed to update special list due to database constraint", status_code=400) from e
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to update special list: {str(e)}", status_code=500) from e

    @staticmethod
    async def delete_special_list(list_id: UUID, user_id: UUID) -> None:
        try:
            records = await SpecialList.select(id=list_id)
            if not records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)
            await SpecialList.delete(id=list_id)
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to delete special list: {str(e)}", status_code=500) from e

    @staticmethod
    async def add_item_to_list(list_id: UUID, user_id: UUID, data: AddSpecialListItemCommand) -> SpecialListItem:
        try:
            list_records = await SpecialList.select(id=list_id)
            if not list_records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = list_records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)

            if data.itemId:
                item_records = await Item.select(id=data.itemId)
                if not item_records:
                    raise SpecialListError("Item not found", status_code=404)
                item = item_records[0]
            else:
                item_records = await Item.select(name=data.name)
                if not item_records:
                    item = await Item.create(name=data.name, weight=data.weight, dimensions=data.dimensions, category=data.category)
                else:
                    item = item_records[0]

            association_records = await SpecialListItem.select(special_list_id=list_id, item_id=item.id)
            if association_records:
                raise SpecialListError("Item already exists in list", status_code=409)

            special_list_item = await SpecialListItem.create(special_list_id=list_id, item_id=item.id, quantity=data.quantity)
            return special_list_item
        except IntegrityError as e:
            raise SpecialListError("Failed to add item due to database constraint", status_code=400) from e
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to add item to list: {str(e)}", status_code=500) from e

    @staticmethod
    async def remove_item_from_list(list_id: UUID, item_id: UUID, user_id: UUID) -> None:
        try:
            list_records = await SpecialList.select(id=list_id)
            if not list_records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = list_records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)

            association_records = await SpecialListItem.select(special_list_id=list_id, item_id=item_id)
            if not association_records:
                raise SpecialListError("Item not found in list", status_code=404)

            await SpecialListItem.delete(id=association_records[0].id)
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to remove item from list: {str(e)}", status_code=500) from e

    @staticmethod
    async def update_list_item_quantity(list_id: UUID, item_id: UUID, user_id: UUID, data: UpdateSpecialListItemCommand) -> SpecialListItem:
        try:
            list_records = await SpecialList.select(id=list_id)
            if not list_records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = list_records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)

            association_records = await SpecialListItem.select(special_list_id=list_id, item_id=item_id)
            if not association_records:
                raise SpecialListError("Item not found in list", status_code=404)

            association = association_records[0]
            association.quantity = data.quantity
            await association.save()
            updated_association = (await SpecialListItem.select(id=association.id))[0]
            return updated_association
        except IntegrityError as e:
            raise SpecialListError("Failed to update item quantity due to database constraint", status_code=400) from e
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to update item quantity: {str(e)}", status_code=500) from e

    @staticmethod
    async def add_tag_to_list(list_id: UUID, user_id: UUID, data: AddTagCommand) -> Tag:
        if not data.has_valid_input:
            raise SpecialListError("Either tag ID or tag name must be provided", status_code=400)

        try:
            list_records = await SpecialList.select(id=list_id)
            if not list_records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = list_records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)

            if data.tagId:
                tag_records = await Tag.select(id=data.tagId)
                if not tag_records:
                    raise SpecialListError("Tag not found", status_code=404)
                tag = tag_records[0]
            else:
                tag_records = await Tag.select(name=data.name)
                if not tag_records:
                    tag = await Tag.create(name=data.name)
                else:
                    tag = tag_records[0]

            if tag in special_list.tags:
                raise SpecialListError("Tag already exists in list", status_code=409)

            special_list.tags.append(tag)
            await special_list.save()
            updated_tag_records = await Tag.select(id=tag.id)
            return updated_tag_records[0]
        except IntegrityError as e:
            raise SpecialListError("Failed to add tag due to database constraint", status_code=400) from e
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to add tag to list: {str(e)}", status_code=500) from e

    @staticmethod
    async def remove_tag_from_list(list_id: UUID, tag_id: UUID, user_id: UUID) -> None:
        try:
            list_records = await SpecialList.select(id=list_id)
            if not list_records:
                raise SpecialListError("Special list not found", status_code=404)
            special_list = list_records[0]
            if special_list.user_id != user_id:
                raise SpecialListError("Access denied", status_code=403)

            tag_records = await Tag.select(id=tag_id)
            if not tag_records:
                raise SpecialListError("Tag not found", status_code=404)
            tag = tag_records[0]

            if tag not in special_list.tags:
                raise SpecialListError("Tag not found in list", status_code=404)

            special_list.tags.remove(tag)
            await special_list.save()
        except SpecialListError as se:
            raise se
        except Exception as e:
            raise SpecialListError(f"Failed to remove tag from list: {str(e)}", status_code=500) from e 