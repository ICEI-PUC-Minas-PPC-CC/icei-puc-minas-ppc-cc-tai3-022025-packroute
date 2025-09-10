from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Location:
    lat: float
    lng: float
    address: Optional[str] = None

@dataclass
class Order:
    id: str
    pickup: Optional[Location]  # pode ser None p/ apenas drop-off
    dropoff: Location
    value: float
    service_time_min: float = 0.0
    earliest: Optional[str] = None  # "HH:MM"
    latest: Optional[str] = None
    weight: float = 0.0

@dataclass
class Vehicle:
    id: str
    start: Location
    end: Optional[Location] = None
    capacity: float = 0.0
