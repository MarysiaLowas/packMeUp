from enum import Enum
from typing import List, Tuple


class AccommodationType(str, Enum):
    HOTEL = "hotel"
    APARTMENT = "apartment"
    CAMPING = "camping"
    HOSTEL = "hostel"
    OTHER = "other"


class TransportType(str, Enum):
    CAR = "car"
    PLANE = "plane"
    TRAIN = "train"
    ON_FOOT = "on_foot"
    BUS = "bus"
    OTHER = "other"


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
    DINNER_OUTSIDE = 3


CATERING_OPTIONS: List[Tuple[int, str]] = [
    (CateringType.FULL.value, "All inclusive"),
    (CateringType.BREAKFAST.value, "Tylko śniadanie"),
    (CateringType.FULL_OWN.value, "Własne wyżywienie"),
    (CateringType.DINNER_OUTSIDE.value, "Kolacja na mieście"),
]
