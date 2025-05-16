import json
import logging
import re
from typing import Dict, List, Optional

from app.models import SpecialList, Trip
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
                "max_tokens": 2048,  # Increased token limit for complete lists
                "top_p": 0.9,  # High top_p for focused but slightly creative outputs
                "frequency_penalty": 0.1,  # Slight penalty to avoid repetition
            }
        )

    @staticmethod
    def _clean_json_content(content: str) -> str:
        """Clean and extract valid JSON from the LLM response."""
        logger.debug("Cleaning JSON content")

        try:
            # Log the first part of the content for debugging
            preview = content[:200] if len(content) > 200 else content
            logger.debug(f"Content to clean (preview): {preview}...")

            # Try to extract JSON array from content
            json_pattern = r"\[.*\]"
            array_match = re.search(json_pattern, content, re.DOTALL)

            if array_match:
                logger.debug("Found JSON array pattern")
                extracted_json = array_match.group(0)

                # Try to parse it to verify it's valid
                try:
                    json.loads(extracted_json)
                    logger.debug("Extracted JSON is valid")
                    return extracted_json
                except json.JSONDecodeError:
                    logger.warning(
                        "Extracted JSON array is not valid, attempting repairs"
                    )
            else:
                logger.warning("No JSON array pattern found in content")
                extracted_json = content

            # Remove markdown code block markers if present
            if "```json" in extracted_json:
                logger.debug("Removing markdown code block markers")
                extracted_json = re.sub(r"```json\s*", "", extracted_json)
                extracted_json = re.sub(r"```\s*", "", extracted_json)

            # Find the first [ and last ]
            start_idx = extracted_json.find("[")
            end_idx = extracted_json.rfind("]")

            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                logger.debug(f"Trimming content from index {start_idx} to {end_idx+1}")
                extracted_json = extracted_json[start_idx : end_idx + 1]
            else:
                logger.warning("Could not find matching [ and ] in content")

            # Remove any trailing or leading commas before closing brackets
            extracted_json = re.sub(r",\s*}", "}", extracted_json)
            extracted_json = re.sub(r",\s*]", "]", extracted_json)

            # Fix missing closing braces
            open_braces = extracted_json.count("{")
            close_braces = extracted_json.count("}")

            if open_braces > close_braces:
                logger.debug(
                    f"Adding {open_braces - close_braces} missing close braces"
                )
                extracted_json += "}" * (open_braces - close_braces)

            # Fix missing closing brackets
            open_brackets = extracted_json.count("[")
            close_brackets = extracted_json.count("]")

            if open_brackets > close_brackets:
                logger.debug(
                    f"Adding {open_brackets - close_brackets} missing close brackets"
                )
                extracted_json += "]" * (open_brackets - close_brackets)

            # Try to parse the result to verify it's valid JSON
            try:
                result = json.loads(extracted_json)
                logger.debug("Successfully parsed cleaned JSON")

                # If it's not a list, but we expect a list, wrap it
                if not isinstance(result, list):
                    logger.debug("Result is not a list, wrapping it")
                    return json.dumps([result])

                return extracted_json
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse cleaned JSON: {str(e)}")
                # Last resort - return simple empty array
                logger.debug("Returning empty array as fallback")
                return "[]"

        except Exception as e:
            logger.error(f"Error cleaning JSON content: {str(e)}")
            return "[]"

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

        # Safely log trip.children_ages
        try:
            children_str = str(trip.children_ages) if trip.children_ages else "None"
        except Exception as e:
            logger.warning(f"Error logging children_ages: {str(e)}")

        # Safely log trip.activities
        try:
            activities_str = (
                ", ".join(trip.activities)
                if trip.activities and isinstance(trip.activities, list)
                else "Not specified"
            )
        except Exception as e:
            logger.warning(f"Error joining activities: {str(e)}")

        # Build prompt with trip details
        try:
            logger.debug("Building prompt")
            # Safe string representation, escaping any format specifiers

            dest = (
                str(trip.destination).replace("{", "{{").replace("}", "}}")
                if trip.destination
                else "Not specified"
            )
            days = (
                str(trip.duration_days).replace("{", "{{").replace("}", "}}")
                if trip.duration_days
                else "0"
            )
            adults = (
                str(trip.num_adults).replace("{", "{{").replace("}", "}}")
                if trip.num_adults
                else "0"
            )

            children_safe = (
                str(trip.children_ages).replace("{", "{{").replace("}", "}}")
                if trip.children_ages
                else "None"
            )
            accommodation_safe = (
                str(trip.accommodation).replace("{", "{{").replace("}", "}}")
                if trip.accommodation
                else "Not specified"
            )
            transport_safe = (
                str(trip.transport).replace("{", "{{").replace("}", "}}")
                if trip.transport
                else "Not specified"
            )

            # Handle activities safely
            if trip.activities and isinstance(trip.activities, list):
                try:
                    activities_joined = ", ".join(
                        str(a).replace("{", "{{").replace("}", "}}")
                        for a in trip.activities
                    )
                except Exception as e:
                    logger.error(f"Error formatting activities: {str(e)}")
                    activities_joined = "Not specified"
            else:
                activities_joined = "Not specified"

            season_safe = (
                str(trip.season).replace("{", "{{").replace("}", "}}")
                if trip.season
                else "Not specified"
            )

            prompt = f"""
Wygeneruj listę rzeczy do spakowania na podróż o następujących szczegółach:
- Cel podróży: {dest}
- Czas trwania: {days} dni
- Liczba dorosłych: {adults}
- Wiek dzieci: {children_safe} (lista wieków dzieci, np. [], [2, 5], jeśli brak dzieci, lista będzie pusta)
- Zakwaterowanie: {accommodation_safe} (np. hotel, apartament z kuchnią, kemping)
- Transport: {transport_safe}(np. samolot, samochód, pociąg)
- Aktywności: {activities_joined} (np. plażowanie, zwiedzanie miasta, trekking, spotkania biznesowe)
- Pora roku: {season_safe} (np. lato, zima, wiosna, jesień)

Dla każdego przedmiotu na liście, zwróć obiekt JSON z następującymi **kluczami w języku angielskim**:
- `name`: (string) Jasna i konkretna **nazwa przedmiotu w języku polskim**.
- `quantity`: (integer) Wymagana liczba sztuk, obliczona na podstawie czasu trwania podróży i liczby podróżujących. Dla przedmiotów, których dokładna ilość jest trudna do ustalenia z góry (np. krem z filtrem, pasta do zębów, płyn pod prysznic) lub których ilość jest "jedna sztuka zbiorcza" (np. apteczka, kosmetyczka), użyj wartości 1. Dostosuj ilość ubrań (np. skarpetki, bielizna) do długości wyjazdu oraz dostępności prania.
- `category`: (string) Jedna z predefiniowanych **polskich nazw kategorii**: "Odzież", "Elektronika", "Kosmetyki", "Dokumenty", "Akcesoria", "Zdrowie", "Rozrywka".
- `weight`: (number, opcjonalnie) Przybliżona waga w kg. Staraj się podać dla jak największej liczby przedmiotów, zwłaszcza jeśli są ograniczenia bagażowe. Użyj kropki jako separatora dziesiętnego.

Przykład pojedynczego obiektu JSON:
`{{"name": "Pasta do zębów", "quantity": 1, "category": "Kosmetyki", "weight": 0.1}}`

Sformatuj odpowiedź jako tablicę JSON tych obiektów.
Upewnij się, że wszystkie wartości dla klucza `quantity` są liczbami całkowitymi, a dla klucza `weight` liczbami (mogą być dziesiętne).
Upewnij się, że całkowita waga nie przekracza limitów bagażu, jeśli zostały określone.
Nie umieszczaj tablicy JSON w żadnym dodatkowym obiekcie nadrzędnym.
Klucze w obiektach JSON muszą być w języku angielskim, a **wartości tekstowe (takie jak wartości dla kluczy `name` i `category`) muszą być w języku polskim.**
"""
            logger.debug("Prompt built successfully")
        except Exception as e:
            logger.error(f"Error building prompt: {str(e)}")
            # Fallback to a simpler prompt
            prompt = """
Wygeneruj listę rzeczy do spakowania na podróż.
Dla każdego przedmiotu zwróć obiekt JSON z następującymi kluczami:
- name: Nazwa przedmiotu po polsku
- quantity: Liczba sztuk (liczba całkowita)
- category: Kategoria (po polsku): Odzież, Elektronika, Kosmetyki, Dokumenty, Akcesoria, Zdrowie, Rozrywka
- weight: Przybliżona waga w kg (opcjonalnie)

Przykład: {"name": "Pasta do zębów", "quantity": 1, "category": "Kosmetyki", "weight": 0.1}
"""

        if trip.available_luggage:
            try:
                logger.debug(
                    f"Adding luggage constraints, type: {type(trip.available_luggage).__name__}"
                )
                prompt += "\nOgraniczenia bagażowe:\n"

                # Ensure we're dealing with a list or convert to list if it's a single item
                if not isinstance(trip.available_luggage, list):
                    luggage_items = [trip.available_luggage]
                else:
                    luggage_items = trip.available_luggage

                for i, luggage in enumerate(luggage_items):
                    logger.debug(
                        f"Processing luggage item {i+1}, type: {type(luggage).__name__}"
                    )
                    # Try different ways to access luggage data
                    if isinstance(luggage, dict):
                        logger.debug(f"Luggage keys: {list(luggage.keys())}")
                        if "max_weight" in luggage:
                            weight_val = (
                                str(luggage["max_weight"])
                                .replace("{", "{{")
                                .replace("}", "}}")
                            )
                            prompt += f"- Maksymalna waga: {weight_val} kg\n"
                        if "maxWeight" in luggage:  # Try alternative property name
                            weight_val = (
                                str(luggage["maxWeight"])
                                .replace("{", "{{")
                                .replace("}", "}}")
                            )
                            prompt += f"- Maksymalna waga: {weight_val} kg\n"
                        if "dimensions" in luggage:
                            dim_val = (
                                str(luggage["dimensions"])
                                .replace("{", "{{")
                                .replace("}", "}}")
                            )
                            prompt += f"- Wymiary: {dim_val}\n"
                    elif hasattr(luggage, "max_weight") and luggage.max_weight:
                        weight_val = (
                            str(luggage.max_weight)
                            .replace("{", "{{")
                            .replace("}", "}}")
                        )
                        prompt += f"- Maksymalna waga: {weight_val} kg\n"
                    elif hasattr(luggage, "maxWeight") and luggage.maxWeight:
                        weight_val = (
                            str(luggage.maxWeight).replace("{", "{{").replace("}", "}}")
                        )
                        prompt += f"- Maksymalna waga: {weight_val} kg\n"

                    if hasattr(luggage, "dimensions") and luggage.dimensions:
                        dim_val = (
                            str(luggage.dimensions)
                            .replace("{", "{{")
                            .replace("}", "}}")
                        )
                        prompt += f"- Wymiary: {dim_val}\n"
            except Exception as e:
                logger.error(f"Error adding luggage constraints: {str(e)}")

        # Set user message
        try:
            logger.debug("Setting user message on OpenRouter client")
            ai_service.openrouter.set_user_message(prompt)
        except Exception as e:
            logger.error(f"Error setting user message: {str(e)}")
            raise ValueError(f"Failed to set user message: {str(e)}")

        try:
            # Call the API
            logger.debug("Calling OpenRouter API to generate packing list")
            response = await ai_service.openrouter.ask()
            logger.debug("OpenRouter API call completed")

            # Process and parse the response
            logger.debug("Processing AI response")
            items = []

            try:
                logger.debug(f"Raw AI response type: {type(response).__name__}")
                json_str = response

                # Log the first 200 chars of response for debugging
                safe_preview = str(json_str)[:200].replace("{", "{{").replace("}", "}}")
                logger.debug(f"Response preview: {safe_preview}...")

                try:
                    logger.debug("Cleaning and parsing JSON response")

                    # Clean and prepare the JSON before parsing
                    cleaned_json = AIService._clean_json_content(json_str)
                    logger.debug("JSON content cleaned, attempting to parse")

                    parsed_items = json.loads(cleaned_json)

                    if not isinstance(parsed_items, list):
                        logger.warning(
                            "Parsed response is not a list, wrapping in list"
                        )
                        parsed_items = [parsed_items]

                    logger.debug(
                        f"Successfully parsed {len(parsed_items)} items from response"
                    )

                    # Process each item
                    for i, item in enumerate(parsed_items):
                        try:
                            logger.debug(
                                f"Processing item {i+1}: {item.get('name', 'Unknown')}"
                            )

                            # Ensure required fields exist
                            if "name" not in item:
                                logger.warning(
                                    f"Item {i+1} missing 'name' field, skipping"
                                )
                                continue

                            if "category" not in item:
                                logger.warning(
                                    f"Item {i+1} '{item['name']}' missing 'category' field, adding default"
                                )
                                item["category"] = "Inne"

                            # Process quantity field
                            if "quantity" not in item:
                                logger.warning(
                                    f"Item {i+1} '{item['name']}' missing 'quantity' field, setting to 1"
                                )
                                item["quantity"] = 1
                            else:
                                # Ensure quantity is an integer
                                try:
                                    quantity_value = item["quantity"]
                                    if not isinstance(quantity_value, int):
                                        logger.warning(
                                            f"Item {i+1} '{item['name']}' has non-integer quantity: {quantity_value}, converting"
                                        )
                                        item["quantity"] = int(float(quantity_value))
                                except (ValueError, TypeError) as e:
                                    logger.error(
                                        f"Error converting quantity for '{item['name']}': {str(e)}"
                                    )
                                    item["quantity"] = 1

                            # Add weight if missing
                            if "weight" not in item:
                                logger.debug(
                                    f"Item {i+1} '{item['name']}' missing 'weight' field"
                                )
                            else:
                                # Ensure weight is a number
                                try:
                                    weight_value = item["weight"]
                                    if not isinstance(weight_value, (int, float)):
                                        logger.warning(
                                            f"Item {i+1} '{item['name']}' has non-numeric weight: {weight_value}, converting"
                                        )
                                        item["weight"] = float(weight_value)
                                except (ValueError, TypeError) as e:
                                    logger.error(
                                        f"Error converting weight for '{item['name']}': {str(e)}"
                                    )
                                    item.pop("weight", None)  # Remove invalid weight

                            # Add the processed item
                            items.append(item)

                        except Exception as e:
                            logger.error(f"Error processing item {i+1}: {str(e)}")

                    logger.debug(f"Final processed item count: {len(items)}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {str(e)}")
                    logger.error(f"Invalid JSON: {json_str}")
                    # Try to extract anything that looks like items from the malformed response
                    items = ai_service._extract_items_from_text(json_str)
                    logger.debug(
                        f"Extracted {len(items)} items from malformed response"
                    )
            except Exception as e:
                logger.error(f"Error processing AI response: {str(e)}")

            # Adjust quantities for adults and children
            try:
                if trip.num_adults > 1 or (
                    trip.children_ages and len(trip.children_ages) > 0
                ):
                    logger.debug("Adjusting quantities for multiple people")
                    for item in items:
                        try:
                            # Adjust quantities for personal items
                            category_en = item.get("category", "")
                            category_pl = item.get("category", "")

                            # Check both English and Polish category names
                            is_personal = any(
                                cat in category_en.lower() or cat in category_pl.lower()
                                for cat in [
                                    "odzież",
                                    "kosmetyki",
                                    "zdrowie",
                                    "clothes",
                                    "cosmetics",
                                    "health",
                                ]
                            )

                            if is_personal:
                                logger.debug(f"Adjusting personal item: {item['name']}")
                                # Try to get current quantity safely
                                try:
                                    current_qty = int(item.get("quantity", 1))
                                except (ValueError, TypeError):
                                    logger.warning(
                                        f"Non-integer quantity for {item['name']}, resetting to 1"
                                    )
                                    current_qty = 1

                                # Calculate new quantity
                                num_people = trip.num_adults
                                if trip.children_ages:
                                    num_people += len(trip.children_ages)

                                logger.debug(
                                    f"Adjusting quantity for {item['name']} from {current_qty} to {current_qty * num_people} for {num_people} people"
                                )
                                item["quantity"] = current_qty * num_people
                        except Exception as e:
                            logger.error(
                                f"Error adjusting quantity for {item.get('name', 'Unknown')}: {str(e)}"
                            )
            except Exception as e:
                logger.error(f"Error during quantity adjustment: {str(e)}")

            # TODO: Add items from special lists if provided
            # Add items from special lists if provided
            # if special_lists:
            #     try:
            #         logger.debug(
            #             f"Adding items from {len(special_lists)} special lists"
            #         )
            #         for special_list in special_lists:
            #             logger.debug(f"Processing special list: {special_list.name}")
            #             for item in special_list.items:
            #                 try:
            #                     # Create a dictionary for the item
            #                     special_item = {
            #                         "name": item.name,
            #                         "quantity": item.quantity,
            #                         "category": item.category,
            #                     }

            #                     if item.weight:
            #                         special_item["weight"] = item.weight

            #                     logger.debug(
            #                         f"Adding special item: {special_item['name']}"
            #                     )
            #                     items.append(special_item)
            #                 except Exception as e:
            #                     logger.error(f"Error adding special item: {str(e)}")
            #     except Exception as e:
            #         logger.error(f"Error processing special lists: {str(e)}")

            # Exclude categories if provided
            if exclude_categories:
                try:
                    logger.debug(f"Excluding categories: {exclude_categories}")
                    original_count = len(items)
                    items = [
                        item
                        for item in items
                        if item.get("category", "").lower()
                        not in [cat.lower() for cat in exclude_categories]
                    ]
                    logger.debug(
                        f"Removed {original_count - len(items)} items from excluded categories"
                    )
                except Exception as e:
                    logger.error(f"Error excluding categories: {str(e)}")

            logger.debug(f"Returning {len(items)} items in packing list")
            return items

        except Exception as e:
            logger.error(f"Error generating packing list: {str(e)}")
            # Return a minimal default list in case of failure
            return [
                {"name": "Ubrania na zmianę", "quantity": 1, "category": "Odzież"},
                {
                    "name": "Szczoteczka do zębów",
                    "quantity": 1,
                    "category": "Kosmetyki",
                },
                {"name": "Dokumenty", "quantity": 1, "category": "Dokumenty"},
                {
                    "name": "Ładowarka do telefonu",
                    "quantity": 1,
                    "category": "Elektronika",
                },
            ]

    @staticmethod
    def _extract_items_from_text(text: str) -> List[Dict]:
        """Extract items from malformed JSON or text response."""
        logger.debug("Attempting to extract items from malformed response")
        items = []

        try:
            # Try to find JSON-like objects in the text
            matches = re.finditer(
                r'{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"quantity"\s*:\s*(\d+)\s*,\s*"category"\s*:\s*"([^"]+)"',
                text,
            )

            for match in matches:
                try:
                    name = match.group(1)
                    quantity = int(match.group(2))
                    category = match.group(3)

                    logger.debug(f"Extracted item: {name}")
                    items.append(
                        {"name": name, "quantity": quantity, "category": category}
                    )
                except Exception as e:
                    logger.error(f"Error extracting item from regex match: {str(e)}")

            logger.debug(f"Extracted {len(items)} items using regex")
        except Exception as e:
            logger.error(f"Error extracting items from text: {str(e)}")

        return items
