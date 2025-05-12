from typing import Dict, List, Optional
from uuid import UUID

from app.models import Trip, SpecialList

class AIService:
    """Service for AI-powered features like packing list generation."""
    
    MOCK_ITEMS = [
        {
            "name": "Toothbrush",
            "quantity": 1,
            "category": "Hygiene",
            "weight": 0.1
        },
        {
            "name": "T-shirt",
            "quantity": 3,
            "category": "Clothing",
            "weight": 0.2
        },
        {
            "name": "Passport",
            "quantity": 1,
            "category": "Documents",
            "weight": 0.1
        },
        {
            "name": "Phone Charger",
            "quantity": 1,
            "category": "Electronics",
            "weight": 0.2
        },
        {
            "name": "First Aid Kit",
            "quantity": 1,
            "category": "Health",
            "weight": 0.5
        }
    ]
    
    ACTIVITY_ITEMS = {
        "sightseeing": [
            {"name": "Comfortable Walking Shoes", "quantity": 1, "category": "Clothing", "weight": 0.8},
            {"name": "Camera", "quantity": 1, "category": "Electronics", "weight": 0.5},
            {"name": "Water Bottle", "quantity": 1, "category": "Accessories", "weight": 0.3}
        ],
        "swimming": [
            {"name": "Swimsuit", "quantity": 1, "category": "Clothing", "weight": 0.2},
            {"name": "Beach Towel", "quantity": 1, "category": "Accessories", "weight": 0.5},
            {"name": "Sunscreen", "quantity": 1, "category": "Health", "weight": 0.2}
        ],
        "hiking": [
            {"name": "Hiking Boots", "quantity": 1, "category": "Clothing", "weight": 1.0},
            {"name": "Backpack", "quantity": 1, "category": "Accessories", "weight": 1.0},
            {"name": "Rain Jacket", "quantity": 1, "category": "Clothing", "weight": 0.5}
        ]
    }
    
    @staticmethod
    async def generate_packing_list(
        trip: Trip,
        special_lists: Optional[List[SpecialList]] = None,
        exclude_categories: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Generate a packing list based on trip details and optional parameters.
        Currently returns mocked data - will be replaced with actual AI model later.
        
        Args:
            trip: Trip object with all details
            special_lists: Optional list of special lists to include items from
            exclude_categories: Optional list of categories to exclude
            
        Returns:
            List of dictionaries containing item details
        """
        # Start with basic items
        items = AIService.MOCK_ITEMS.copy()
        
        # Add items based on activities
        if trip.activities:
            for activity in trip.activities:
                activity_lower = activity.lower()
                if activity_lower in AIService.ACTIVITY_ITEMS:
                    items.extend(AIService.ACTIVITY_ITEMS[activity_lower])
        
        # Add items from special lists if provided
        if special_lists:
            for special_list in special_lists:
                for item in special_list.items:
                    items.append({
                        "item_id": item.item_id,
                        "name": item.item.name if item.item else "Custom Item",
                        "quantity": item.quantity,
                        "category": item.item.category if item.item else None,
                        "weight": item.item.weight if item.item else None,
                        "dimensions": item.item.dimensions if item.item else None
                    })
        
        # Filter out excluded categories
        if exclude_categories:
            items = [
                item for item in items 
                if not item.get("category") or item["category"] not in exclude_categories
            ]
        
        # Adjust quantities based on number of people
        for item in items:
            if item["category"] in ["Clothing", "Hygiene"]:
                item["quantity"] *= trip.num_adults
                if trip.children_ages:
                    item["quantity"] += len(trip.children_ages)
        
        return items 