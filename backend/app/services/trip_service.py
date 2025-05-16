from datetime import date
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.dto import GeneratePackingListResponseDTO
from app.models import GeneratedList, GeneratedListItem, Trip
from app.services.ai_service import AIService
from app.services.special_list_service import SpecialListService


class TripService:
    ALLOWED_SORT_FIELDS = {"created_at", "destination", "start_date", "duration_days"}

    @staticmethod
    async def create_trip(
        user_id: UUID,
        destination: str,
        duration_days: int,
        start_date: Optional[date] = None,
        **kwargs,
    ) -> Trip:
        """Create a new trip with basic validation.

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
            **kwargs,
        }

        # Create trip and return its ID
        trip_id = await Trip.create(**trip_data)

        # Fetch and return the complete Trip object
        return await Trip.get(id=trip_id)

    @staticmethod
    async def list_trips(
        user_id: UUID, limit: int = 10, offset: int = 0, sort: Optional[str] = None
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
        exclude_categories: Optional[List[str]] = None,
    ) -> "GeneratePackingListResponseDTO":
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
        # Setup logging
        import logging

        logger = logging.getLogger("trip_service")
        logger.setLevel(logging.DEBUG)
        # Create console handler if it doesn't exist
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        try:
            logger.debug(f"Starting generate_packing_list for trip ID: {trip.id}")
            logger.debug(
                f"Trip data: dest={trip.destination}, days={trip.duration_days}, adults={trip.num_adults}"
            )

            # Verify trip ownership again as a safeguard
            if trip.user_id != user_id:
                logger.error(
                    f"Access denied: Trip owner {trip.user_id} != requester {user_id}"
                )
                raise ValueError("Access denied")

            # Get special lists if specified
            special_lists = []
            if include_special_lists:
                logger.debug(f"Fetching special lists: {include_special_lists}")
                special_lists = await SpecialListService.get_lists(
                    list_ids=include_special_lists, user_id=user_id
                )
                if len(special_lists) != len(include_special_lists):
                    logger.error(
                        f"Special lists not found: requested {len(include_special_lists)}, found {len(special_lists)}"
                    )
                    raise ValueError("One or more special lists not found")

            # Generate list name based on trip destination
            try:
                logger.debug(
                    f"Creating list name for destination: '{trip.destination}'"
                )
                # Handle potential formatting issues with curly braces
                dest = str(trip.destination).replace("{", "{{").replace("}", "}}")
                list_name = f"Packing List for {dest}"
                logger.debug(f"List name created: '{list_name}'")
            except Exception as e:
                logger.error(f"Error creating list name: {str(e)}")
                list_name = "Packing List"

            # Create generated list entry
            try:
                logger.debug(
                    f"Creating GeneratedList: user_id={user_id}, trip_id={trip.id}, name='{list_name}'"
                )
                generated_list_id = await GeneratedList.create(
                    user_id=user_id, trip_id=trip.id, name=list_name
                )
                logger.debug(f"GeneratedList created with ID: {generated_list_id}")
            except Exception as e:
                logger.error(f"Error creating GeneratedList: {str(e)}")
                raise Exception(f"Failed to create generated list: {str(e)}")

            try:
                # Call AI service to generate items
                logger.debug("Calling AI service to generate packing list")
                generated_items = await AIService.generate_packing_list(
                    trip=trip,
                    special_lists=special_lists,
                    exclude_categories=exclude_categories,
                )
                logger.debug(f"AI service returned {len(generated_items)} items")

                # Create generated list items
                for i, item in enumerate(generated_items):
                    try:
                        logger.debug(
                            f"Creating item {i+1}/{len(generated_items)}: {item.get('name', 'unknown')}"
                        )
                        item_weight = None
                        if item.get("weight") is not None:
                            try:
                                item_weight = float(item["weight"])
                            except (ValueError, TypeError) as e:
                                logger.warning(
                                    f"Invalid weight value '{item.get('weight')}': {str(e)}"
                                )

                        await GeneratedListItem.create(
                            generated_list_id=generated_list_id,
                            item_id=item.get("item_id"),  # May be None for custom items
                            item_name=item["name"],
                            quantity=item.get("quantity", 1),
                            is_packed=False,
                            item_category=item.get("category"),
                            item_weight=item_weight,
                            item_dimensions=item.get("dimensions"),
                        )
                    except Exception as e:
                        logger.error(f"Error creating item {i+1}: {str(e)}")
                        # Continue with next item instead of failing the whole process
                        continue

                # Fetch the complete list with items
                logger.debug(
                    f"Fetching complete list with items for ID: {generated_list_id}"
                )
                query = (
                    select(GeneratedList)
                    .where(GeneratedList.id == generated_list_id)
                    .options(selectinload(GeneratedList.items))
                )
                result = await GeneratedList.select_one(query)
                if not result:
                    logger.error(
                        f"Failed to load generated list with ID: {generated_list_id}"
                    )
                    raise Exception("Failed to load generated list with items")

                logger.debug(
                    f"Successfully fetched list with {len(result.items) if hasattr(result, 'items') else 0} items"
                )

                # Convert to DTO and return
                logger.debug("Converting result to DTO")
                dto = GeneratePackingListResponseDTO.model_validate(
                    result, from_attributes=True
                )
                logger.debug("Successfully generated packing list")
                return dto

            except Exception as e:
                logger.error(f"Error during list generation: {str(e)}")
                # Clean up generated list if something fails
                try:
                    logger.debug(
                        f"Cleaning up generated list with ID: {generated_list_id}"
                    )
                    await GeneratedList.delete(id=generated_list_id)
                except Exception as cleanup_error:
                    logger.error(f"Error during cleanup: {str(cleanup_error)}")
                raise Exception(f"Failed to generate packing list: {str(e)}")

        except Exception as outer_e:
            logger.error(f"Outer exception in generate_packing_list: {str(outer_e)}")
            raise
