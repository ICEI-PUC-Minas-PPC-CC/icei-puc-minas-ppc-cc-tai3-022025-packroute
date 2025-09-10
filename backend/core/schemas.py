# backend/core/schemas.py
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, model_validator

class LocationIn(BaseModel):
    lat: float
    lng: float
    address: Optional[str] = None

class OrderIn(BaseModel):
    id: str
    # Pode vir por coordenadas OU por endereço (geocoding fake no servidor)
    dropoff: Optional[LocationIn] = None
    dropoff_address: Optional[str] = None
    pickup: Optional[LocationIn] = None
    value: float = Field(ge=0, default=0)
    service_time_min: float = 0
    earliest: Optional[str] = None  # "08:00"
    latest: Optional[str] = None
    weight: float = 0

    # Pydantic v2: use model_validator
    @model_validator(mode="after")
    def _check_dropoff(self):
        if self.dropoff is None and not self.dropoff_address:
            raise ValueError("Informe 'dropoff' (lat/lng) ou 'dropoff_address'.")
        return self

class VehicleIn(BaseModel):
    id: str
    start: LocationIn
    end: Optional[LocationIn] = None
    capacity: float = 0

class OptimizeRequest(BaseModel):
    orders: List[OrderIn]
    vehicles: List[VehicleIn] = []
    objective: Literal["min_time", "min_distance", "max_profit"] = "min_time"
    metric:    Literal["distance", "time"] = "distance"
    return_to_depot: bool = True
    # opcionais (para ETAs)
    speed_kmh: float = 25.0
    start_time_hhmm: Optional[str] = None

class StepOut(BaseModel):
    order_id: Optional[str] = None
    lat: float
    lng: float
    arrival_time: Optional[str] = None
    travel_distance_km: float
    travel_time_min: float

class RouteOut(BaseModel):
    vehicle_id: str
    sequence: List[StepOut]
    total_distance_km: float
    total_time_min: float
    total_value: float

class OptimizeResponse(BaseModel):
    routes: List[RouteOut]
    objective: str
    metric: str
