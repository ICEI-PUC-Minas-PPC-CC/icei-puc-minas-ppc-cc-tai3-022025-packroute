# packroute/backend/services/solver_service.py
from typing import List, Dict, Any
from ..core.models import Order, Vehicle, Location
from ..algoritmo import tsp
from ..core.utils import geocode_address

def _to_orders(order_ins) -> List[Order]:
    def to_loc(l): 
        return Location(lat=l.lat, lng=l.lng, address=l.address)
    orders = []
    for o in order_ins:
        if o.dropoff:
            drop = to_loc(o.dropoff)
        else:
            lat, lng = geocode_address(o.dropoff_address)
            drop = Location(lat=lat, lng=lng, address=o.dropoff_address)

        orders.append(Order(
            id=o.id,
            pickup=to_loc(o.pickup) if o.pickup else None,
            dropoff=drop,
            value=o.value,
            service_time_min=o.service_time_min,
            earliest=o.earliest,
            latest=o.latest,
            weight=o.weight
        ))
    return orders

def _to_vehicles(vehicle_ins) -> List[Vehicle]:
    def to_loc(l):
        return Location(lat=l.lat, lng=l.lng, address=l.address)
    if not vehicle_ins:
        # Centro de SP como default
        return [Vehicle(id="v1", start=Location(lat=-23.550520, lng=-46.633308, address="Centro SP"))]
    return [Vehicle(id=v.id, start=to_loc(v.start), end=to_loc(v.end) if v.end else None, capacity=v.capacity) for v in vehicle_ins]

def solve_tsp_or_vrp(payload) -> Dict[str, Any]:
    orders = _to_orders(payload.orders)
    vehicles = _to_vehicles(payload.vehicles)
    result = tsp.solve(
        orders=orders,
        vehicles=vehicles,
        objective=payload.objective,
        metric=payload.metric,
        return_to_depot=payload.return_to_depot,
        speed_kmh=getattr(payload, "speed_kmh", 25.0),
        start_time_hhmm=getattr(payload, "start_time_hhmm", None),
    )
    return result
