from datetime import date, datetime
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func

from app.models import Trip

class TripService:
    ALLOWED_SORT_FIELDS = {'created_at', 'destination', 'start_date', 'duration_days'}

    @staticmethod
    async def create_trip(
        user_id: UUID,
        destination: str,
        duration_days: int,
        start_date: Optional[date] = None,
        **kwargs
    ) -> Trip:
        """
        Creates a new trip with basic validation.
        Currently returns mocked data for testing purposes.
        
        TODO: Implement full business logic:
        - Validate date ranges
        - Check for overlapping trips
        - Apply user preferences
        - Handle capacity planning
        """
        # For now, just create and return the trip
        trip_data = {
            "user_id": user_id,
            "destination": destination,
            "start_date": start_date,
            "duration_days": duration_days,
            **kwargs
        }
        
        return await Trip.create(**trip_data)

    @staticmethod
    async def list_trips(
        user_id: UUID,
        limit: int = 10,
        offset: int = 0,
        sort: Optional[str] = None
    ) -> Tuple[List[Trip], int]:
        """
        List trips for a user with pagination and sorting.
        
        Args:
            user_id: ID of the user
            limit: Maximum number of trips to return
            offset: Number of trips to skip
            sort: Field to sort by (must be one of ALLOWED_SORT_FIELDS)
            
        Returns:
            Tuple of (list of trips, total count)
            
        Raises:
            ValueError: If sort field is invalid
        """
        # Validate sort field
        if sort and sort not in TripService.ALLOWED_SORT_FIELDS:
            raise ValueError(
                f"Invalid sort field. Allowed fields are: {', '.join(TripService.ALLOWED_SORT_FIELDS)}"
            )
        
        # Build query
        query = select(Trip).where(Trip.user_id == user_id)
        
        # Add sorting if specified
        if sort:
            query = query.order_by(getattr(Trip, sort))
        else:
            # Default sort by created_at desc
            query = query.order_by(Trip.created_at.desc())
        
        # Add pagination
        query = query.offset(offset).limit(limit)
        
        # Execute queries
        trips = await Trip.select(user_id=user_id)
        total = len(trips)
        
        return trips, total 

    @staticmethod
    async def get_trip(trip_id: UUID, user_id: UUID) -> Optional[Trip]:
        """
        Get a single trip by ID and verify ownership.
        
        Args:
            trip_id: ID of the trip to retrieve
            user_id: ID of the user who should own the trip
            
        Returns:
            Trip if found and owned by user, None otherwise
            
        Raises:
            ValueError: If trip_id is invalid
        """
        trip = await Trip.get(id=trip_id)
        
        # Verify ownership
        if trip and trip.user_id != user_id:
            return None
            
        return trip 

    @staticmethod
    async def generate_packing_list(
        trip: Trip,
        user_id: UUID,
        include_special_lists: Optional[List[UUID]] = None,
        exclude_categories: Optional[List[str]] = None
    ) -> 'GeneratedList':
        """
        Generate a packing list for a trip using AI service.
        
        Args:
            trip: Trip object to generate list for
            user_id: ID of the user requesting generation
            include_special_lists: Optional list of special list IDs to include
            exclude_categories: Optional list of categories to exclude
            
        Returns:
            Generated packing list with items
            
        Raises:
            ValueError: If trip is invalid or special lists not found
            Exception: For AI service or database errors
        """
        from app.models import GeneratedList, GeneratedListItem
        from app.services.ai_service import AIService
        from app.services.special_list_service import SpecialListService
        
        # Verify trip ownership again as a safeguard
        if trip.user_id != user_id:
            raise ValueError("Access denied")
            
        # Get special lists if specified
        special_lists = []
        if include_special_lists:
            special_lists = await SpecialListService.get_lists(
                list_ids=include_special_lists,
                user_id=user_id
            )
            # Verify all requested lists were found
            if len(special_lists) != len(include_special_lists):
                raise ValueError("One or more special lists not found")
        
        # Generate list name based on trip destination
        list_name = f"Packing List for {trip.destination}"
        
        # Create generated list entry
        generated_list = await GeneratedList.create(
            user_id=user_id,
            trip_id=trip.id,
            name=list_name
        )
        
        try:
            # Call AI service to generate items
            generated_items = await AIService.generate_packing_list(
                trip=trip,
                special_lists=special_lists,
                exclude_categories=exclude_categories
            )
            
            # Create generated list items
            for item in generated_items:
                await GeneratedListItem.create(
                    generated_list_id=generated_list.id,
                    item_id=item.get('item_id'),  # May be None for custom items
                    quantity=item['quantity'],
                    is_packed=False,
                    item_name=item['name'],
                    item_weight=item.get('weight'),
                    item_dimensions=item.get('dimensions'),
                    item_category=item.get('category')
                )
            
            # Refresh generated list to include items
            from sqlalchemy.orm import selectinload
            query = (
                select(GeneratedList)
                .where(GeneratedList.id == generated_list.id)
                .options(selectinload(GeneratedList.items))
            )
            result = await GeneratedList.select_one(query)
            return result
            
        except Exception as e:
            # Clean up generated list if something fails
            await GeneratedList.delete(id=generated_list.id)
            raise Exception(f"Failed to generate packing list: {str(e)}")
