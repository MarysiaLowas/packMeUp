from enum import Enum
from typing import List, Tuple

class AccommodationType(str, Enum):
    HOTEL = "hotel"
    APARTMENT = "apartment"
    CAMPING = "camping"

class TransportType(str, Enum):
    CAR = "car"
    PLANE = "plane"
    TRAIN = "train"
    ON_FOOT = "on_foot"

class SeasonType(str, Enum):
    SUMMER = "summer"
    WINTER = "winter"
    SPRING = "spring"
    AUTUMN = "autumn"

# Catering options as (value, label) pairs
class CateringType(int, Enum):
    FULL = 0
    BREAKFAST = 1
    FULL_OWN = 2

CATERING_OPTIONS: List[Tuple[int, str]] = [
    (CateringType.FULL.value, "All inclusive"),
    (CateringType.BREAKFAST.value, "Tylko śniadanie"),
    (CateringType.FULL_OWN.value, "Własne wyżywienie")
] 
