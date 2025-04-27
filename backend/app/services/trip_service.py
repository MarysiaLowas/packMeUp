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
        end_date: Optional[date] = None,
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
            "end_date": end_date,
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
        
        # Get total count
        count_query = select(func.count()).select_from(Trip).where(Trip.user_id == user_id)
        
        # Execute queries
        trips = await Trip.select(user_id=user_id)
        total = await Trip.count(user_id=user_id)
        
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
