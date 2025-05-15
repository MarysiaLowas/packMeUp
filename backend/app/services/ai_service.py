import logging
from typing import Dict, List, Optional
from uuid import UUID
import os
import json

from app.models import Trip, SpecialList
from app.services.openrouter_service import OpenRouterService

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler if it doesn't exist
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

class AIService:
    """Service for AI-powered features like packing list generation."""
    
    def __init__(self):
        """Initialize the AIService with OpenRouter client."""
        self.openrouter = OpenRouterService.from_env()
        
        # Set up system message for packing list generation
        self.openrouter.set_system_message("""
You are an expert travel consultant specializing in creating personalized packing lists.
Your task is to generate a detailed packing list based on the trip details provided.
Consider factors like:
- Duration of stay
- Number of travelers (adults and children)
- Destination and season
- Planned activities
- Available luggage capacity
- Accommodation type and catering options
- Mode of transport

For each item, provide:
- name: Clear and specific item name (string)
- quantity: Number needed based on trip duration and travelers (integer, use 1 for variable quantities)
- category: One of [Clothing, Electronics, Toiletries, Documents, Accessories, Health, Entertainment] (string)
- weight: Approximate weight in kg (number, optional)

Format your response as a JSON array of items, each with the above properties.
Ensure all quantities are integers and weights are numbers.
Ensure the total weight stays within luggage limits if specified.
Do not wrap the array in any additional object.
""")
        
        # Set response format schema
        self.openrouter.set_response_format({
            "type": "json_object"
        })
        
        # Set model name (using Mistral-7B for structured output)
        self.openrouter.set_model_name("mistralai/mistral-7b-instruct:free")
        
        # Set model parameters (optimized for JSON generation)
        self.openrouter.set_model_parameters({
            "temperature": 0.1,  # Lower temperature for more consistent JSON
            "max_tokens": 1024,  # Increased token limit for complete lists
            "top_p": 0.9,       # High top_p for focused but slightly creative outputs
            "frequency_penalty": 0.1  # Slight penalty to avoid repetition
        })
    
    @staticmethod
    def _clean_json_content(content: str) -> str:
        """Clean the JSON content by removing markdown code blocks and fixing truncation."""
        logger.debug(f"Cleaning content: {content}")
        
        # Remove markdown code block if present
        if content.startswith('```'):
            # Find the content between ```json and ```
            start_marker = '```json\n'
            if start_marker in content:
                content = content.split(start_marker)[1]
                if '```' in content:
                    content = content.split('```')[0]
            else:
                # Try without json specification
                content = content.split('```')[1]
                if '```' in content:
                    content = content.split('```')[0]

        content = content.strip()
        logger.debug(f"Content after markdown removal: {content}")

        # Fix malformed JSON at the end
        if content.endswith(']}]'):
            content = content[:-3]  # Remove malformed closing brackets
        
        # Find the last complete object
        last_complete_brace = content.rfind('}')
        if last_complete_brace != -1:
            content = content[:last_complete_brace + 1]
            
        # Ensure proper array closure
        if content.count('[') > content.count(']'):
            content += ']'
            
        # Ensure the content starts with [ and ends with ]
        if not content.startswith('['):
            content = '[' + content
        if not content.endswith(']'):
            content = content + ']'

        # Fix any truncated objects at the end
        if '"Name":' in content and not content.endswith('}]'):
            # Find the last complete object
            last_complete = content.rfind('  }')
            if last_complete != -1:
                content = content[:last_complete + 3] + ']'

        logger.debug(f"Final cleaned content: {content}")
        return content

    @staticmethod
    async def generate_packing_list(
        trip: Trip,
        special_lists: Optional[List[SpecialList]] = None,
        exclude_categories: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Generate a packing list based on trip details and optional parameters.
        Uses OpenRouter API to generate personalized recommendations.
        
        Args:
            trip: Trip object with all details
            special_lists: Optional list of special lists to include items from
            exclude_categories: Optional list of categories to exclude
            
        Returns:
            List of dictionaries containing item details
        """
        # Create instance to access OpenRouter
        ai_service = AIService()
        
        # Build prompt with trip details
        prompt = f"""
Generate a packing list for a trip with the following details:
- Destination: {trip.destination}
- Duration: {trip.duration_days} days
- Number of adults: {trip.num_adults}
- Children ages: {trip.children_ages if trip.children_ages else 'None'}
- Accommodation: {trip.accommodation if trip.accommodation else 'Not specified'}
- Transport: {trip.transport if trip.transport else 'Not specified'}
- Activities: {', '.join(trip.activities) if trip.activities else 'Not specified'}
- Season: {trip.season if trip.season else 'Not specified'}
"""

        if trip.available_luggage:
            prompt += "\nLuggage constraints:\n"
            for luggage in trip.available_luggage:
                if luggage.get('max_weight'):
                    prompt += f"- Maximum weight: {luggage['max_weight']} kg\n"
                if luggage.get('dimensions'):
                    prompt += f"- Dimensions: {luggage['dimensions']}\n"
        
        # Set user message
        ai_service.openrouter.set_user_message(prompt)
        
        try:
            # Get AI-generated items
            response = await ai_service.openrouter.send_request()
            logger.debug(f"OpenRouter raw response: {response}")
            
            # Parse response more carefully
            if not response or not isinstance(response, dict):
                logger.error(f"Invalid response format from OpenRouter: {response}")
                raise ValueError("Invalid response format from OpenRouter")
                
            choices = response.get('choices', [])
            if not choices:
                logger.error("No choices in OpenRouter response")
                raise ValueError("No choices in OpenRouter response")
                
            content = choices[0].get('message', {}).get('content', '')
            logger.debug(f"Content from OpenRouter: {content}")
            
            # Clean and parse the content
            try:
                cleaned_content = AIService._clean_json_content(content)
                logger.debug(f"Cleaned content: {cleaned_content}")
                items = json.loads(cleaned_content)
                
                if not isinstance(items, list):
                    logger.error(f"Content is not a list: {items}")
                    raise ValueError("Content is not a list")
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON content: {e}")
                raise ValueError(f"Failed to parse JSON content: {e}")
            
            logger.debug(f"Parsed items: {items}")
            
            # Add items from special lists if provided
            if special_lists:
                for special_list in special_lists:
                    logger.debug(f"Processing special list: {special_list}")
                    if not hasattr(special_list, 'item_associations'):
                        logger.warning(f"Special list {special_list} has no item_associations attribute")
                        continue
                        
                    for item_association in special_list.item_associations:
                        logger.debug(f"Processing item association: {item_association}")
                        items.append({
                            "item_id": item_association.item_id,
                            "name": item_association.item.name if item_association.item else "Custom Item",
                            "quantity": item_association.quantity,
                            "category": item_association.item.category if item_association.item else None,
                            "weight": item_association.item.weight if item_association.item else None,
                            "dimensions": item_association.item.dimensions if item_association.item else None
                        })
            
            # Filter out excluded categories
            if exclude_categories:
                items = [
                    item for item in items 
                    if not item.get("category") or item["category"] not in exclude_categories
                ]
            
            # Adjust quantities based on number of people
            for item in items:
                if item.get("category") in ["Clothing", "Toiletries"]:
                    item["quantity"] *= trip.num_adults
                    if trip.children_ages:
                        item["quantity"] += len(trip.children_ages)
            
            return items
            
        except Exception as e:
            logger.error(f"Error generating packing list: {e}", exc_info=True)
            # Fallback to basic items if AI generation fails
            return [
                {"name": "Toothbrush", "quantity": 1, "category": "Toiletries", "weight": 0.1},
                {"name": "Passport", "quantity": 1, "category": "Documents", "weight": 0.1},
                {"name": "Phone Charger", "quantity": 1, "category": "Electronics", "weight": 0.2},
                {"name": "First Aid Kit", "quantity": 1, "category": "Health", "weight": 0.5}
            ] 