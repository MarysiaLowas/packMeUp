import logging
from typing import Dict, List, Optional
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
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class AIService:
    """Service for AI-powered features like packing list generation."""

    def __init__(self):
        """Initialize the AIService with OpenRouter client."""
        self.openrouter = OpenRouterService.from_env()

        # Set up system message for packing list generation
        self.openrouter.set_system_message(
            """
Jesteś ekspertem ds. podróży, specjalizującym się w tworzeniu spersonalizowanych list rzeczy do spakowania.
Twoim zadaniem jest wygenerowanie szczegółowej listy rzeczy do spakowania na podstawie dostarczonych szczegółów podróży.

Przygotowując listę, weź pod uwagę następujące kluczowe aspekty, aby dostosować ją jak najlepiej:
- Czas trwania pobytu: Dłuższe wyjazdy wymagają więcej ubrań (zwłaszcza bielizny i skarpetek) oraz potencjalnie większych opakowań kosmetyków lub zapasów leków.
- Liczba podróżujących (dorośli i dzieci): Dostosuj liczbę przedmiotów wspólnych (np. apteczka, ładowarki) oraz indywidualnych (ubrania, szczoteczki do zębów). Zwróć szczególną uwagę na potrzeby dzieci w określonym wieku.
- Cel podróży i pora roku: Klimat i pogoda w miejscu docelowym determinują rodzaj odzieży (np. ciepłe kurtki zimą, stroje kąpielowe latem, odzież przeciwdeszczowa). Weź pod uwagę specyfikę kulturową miejsca docelowego (np. odpowiedni strój do miejsc kultu).
- Planowane aktywności: Specjalistyczny sprzęt może być potrzebny do konkretnych działań (np. buty trekkingowe, sprzęt do snorkelingu, elegancki strój na formalne okazje).
- Dostępna pojemność bagażu: Jeśli podano ograniczenia, lista musi być zoptymalizowana pod kątem wagi i objętości. Priorytetyzuj niezbędne rzeczy.
- Rodzaj zakwaterowania i opcje wyżywienia (wynikające z `{{accommodation}}`): Np. w hotelu z zapewnionymi ręcznikami i kosmetykami, można ich nie zabierać. Apartament z kuchnią może sugerować zabranie podstawowych przypraw lub kawy/herbaty, jeśli użytkownik chce samodzielnie przygotowywać posiłki.
- Środek transportu (wynikający z `{{transport}}`): Podróż samochodem daje większą elastyczność bagażową niż samolotem z restrykcyjnymi limitami. Weź to pod uwagę przy sugerowaniu ilości i rodzaju przedmiotów.
"""
        )

        # Set response format schema
        self.openrouter.set_response_format({"type": "json_object"})

        # Set model name (using Mistral-7B for structured output)
        self.openrouter.set_model_name("mistralai/mistral-7b-instruct:free")

        # Set model parameters (optimized for JSON generation)
        self.openrouter.set_model_parameters(
            {
                "temperature": 0.1,  # Lower temperature for more consistent JSON
                "max_tokens": 1024,  # Increased token limit for complete lists
                "top_p": 0.9,  # High top_p for focused but slightly creative outputs
                "frequency_penalty": 0.1,  # Slight penalty to avoid repetition
            }
        )

    @staticmethod
    def _clean_json_content(content: str) -> str:
        """Clean the JSON content by removing markdown code blocks and fixing truncation."""
        logger.debug(f"Cleaning content: {content}")

        # Remove markdown code block if present
        if content.startswith("```"):
            # Find the content between ```json and ```
            start_marker = "```json\n"
            if start_marker in content:
                content = content.split(start_marker)[1]
                if "```" in content:
                    content = content.split("```")[0]
            else:
                # Try without json specification
                content = content.split("```")[1]
                if "```" in content:
                    content = content.split("```")[0]

        content = content.strip()
        logger.debug(f"Content after markdown removal: {content}")

        # Fix malformed JSON at the end
        if content.endswith("]}]"):
            content = content[:-3]  # Remove malformed closing brackets

        # Find the last complete object
        last_complete_brace = content.rfind("}")
        if last_complete_brace != -1:
            content = content[: last_complete_brace + 1]

        # Ensure proper array closure
        if content.count("[") > content.count("]"):
            content += "]"

        # Ensure the content starts with [ and ends with ]
        if not content.startswith("["):
            content = "[" + content
        if not content.endswith("]"):
            content = content + "]"

        # Fix any truncated objects at the end
        if '"Name":' in content and not content.endswith("}]"):
            # Find the last complete object
            last_complete = content.rfind("  }")
            if last_complete != -1:
                content = content[: last_complete + 3] + "]"

        logger.debug(f"Final cleaned content: {content}")
        return content

    @staticmethod
    async def generate_packing_list(
        trip: Trip,
        special_lists: Optional[List[SpecialList]] = None,
        exclude_categories: Optional[List[str]] = None,
    ) -> List[Dict]:
        """
        Generate a packing list based on trip details and optional parameters.

        It uses OpenRouter API to generate personalized recommendations.

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
Wygeneruj listę rzeczy do spakowania na podróż o następujących szczegółach:
- Cel podróży: {trip.destination}
- Czas trwania: {trip.duration_days} dni
- Liczba dorosłych: {trip.num_adults}
- Wiek dzieci: {trip.children_ages if trip.children_ages else 'None'} (lista wieków dzieci, np. [], [2, 5], jeśli brak dzieci, lista będzie pusta)
- Zakwaterowanie: {trip.accommodation if trip.accommodation else 'Not specified'} (np. hotel, apartament z kuchnią, kemping)
- Transport: {trip.transport if trip.transport else 'Not specified'}(np. samolot, samochód, pociąg)
- Aktywności: {', '.join(trip.activities) if trip.activities else 'Not specified'} (np. plażowanie, zwiedzanie miasta, trekking, spotkania biznesowe)
- Pora roku: {trip.season if trip.season else 'Not specified'} (np. lato, zima, wiosna, jesień)

Dla każdego przedmiotu na liście, zwróć obiekt JSON z następującymi **kluczami w języku angielskim**:
- `name`: (string) Jasna i konkretna **nazwa przedmiotu w języku polskim**.
- `quantity`: (integer) Wymagana liczba sztuk, obliczona na podstawie czasu trwania podróży i liczby podróżujących. Dla przedmiotów, których dokładna ilość jest trudna do ustalenia z góry (np. krem z filtrem, pasta do zębów, płyn pod prysznic) lub których ilość jest "jedna sztuka zbiorcza" (np. apteczka, kosmetyczka), użyj wartości 1. Dostosuj ilość ubrań (np. skarpetki, bielizna) do długości wyjazdu oraz dostępności prania.
- `category`: (string) Jedna z predefiniowanych **polskich nazw kategorii**: "Odzież", "Elektronika", "Kosmetyki", "Dokumenty", "Akcesoria", "Zdrowie", "Rozrywka".
- `weight`: (number, opcjonalnie) Przybliżona waga w kg. Staraj się podać dla jak największej liczby przedmiotów, zwłaszcza jeśli są ograniczenia bagażowe. Użyj kropki jako separatora dziesiętnego.

Przykład pojedynczego obiektu JSON:
`{"name": "Pasta do zębów", "quantity": 1, "category": "Kosmetyki", "weight": 0.1}`

Sformatuj odpowiedź jako tablicę JSON tych obiektów.
Upewnij się, że wszystkie wartości dla klucza `quantity` są liczbami całkowitymi, a dla klucza `weight` liczbami (mogą być dziesiętne).
Upewnij się, że całkowita waga nie przekracza limitów bagażu, jeśli zostały określone.
Nie umieszczaj tablicy JSON w żadnym dodatkowym obiekcie nadrzędnym.
Klucze w obiektach JSON muszą być w języku angielskim, a **wartości tekstowe (takie jak wartości dla kluczy `name` i `category`) muszą być w języku polskim.**
"""

        if trip.available_luggage:
            prompt += "\nOgraniczenia bagażowe:\n"
            for luggage in trip.available_luggage:
                if luggage.get("max_weight"):
                    prompt += f"- Maksymalna waga: {luggage['max_weight']} kg\n"
                if luggage.get("dimensions"):
                    prompt += f"- Wymiary: {luggage['dimensions']}\n"

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

            choices = response.get("choices", [])
            if not choices:
                logger.error("No choices in OpenRouter response")
                raise ValueError("No choices in OpenRouter response")

            content = choices[0].get("message", {}).get("content", "")
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
                    if not hasattr(special_list, "item_associations"):
                        logger.warning(
                            f"Special list {special_list} has no item_associations attribute"
                        )
                        continue

                    for item_association in special_list.item_associations:
                        logger.debug(f"Processing item association: {item_association}")
                        items.append(
                            {
                                "item_id": item_association.item_id,
                                "name": (
                                    item_association.item.name
                                    if item_association.item
                                    else "Custom Item"
                                ),
                                "quantity": item_association.quantity,
                                "category": (
                                    item_association.item.category
                                    if item_association.item
                                    else None
                                ),
                                "weight": (
                                    item_association.item.weight
                                    if item_association.item
                                    else None
                                ),
                                "dimensions": (
                                    item_association.item.dimensions
                                    if item_association.item
                                    else None
                                ),
                            }
                        )

            # Filter out excluded categories
            if exclude_categories:
                items = [
                    item
                    for item in items
                    if not item.get("category")
                    or item["category"] not in exclude_categories
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
                {
                    "name": "Toothbrush",
                    "quantity": 1,
                    "category": "Toiletries",
                    "weight": 0.1,
                },
                {
                    "name": "Passport",
                    "quantity": 1,
                    "category": "Documents",
                    "weight": 0.1,
                },
                {
                    "name": "Phone Charger",
                    "quantity": 1,
                    "category": "Electronics",
                    "weight": 0.2,
                },
                {
                    "name": "First Aid Kit",
                    "quantity": 1,
                    "category": "Health",
                    "weight": 0.5,
                },
            ]
