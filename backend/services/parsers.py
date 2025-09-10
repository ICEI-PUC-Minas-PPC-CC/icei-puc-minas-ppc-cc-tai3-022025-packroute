# packroute/backend/services/parsers.py
import csv, io
from fastapi import UploadFile
from ..core.models import Location, Order
from ..core.utils import geocode_address

# Suporta CSV do seu gerador:
# pedido,endereco,valor,janela_inicio,janela_fim  (sem lat/lng)
async def parse_csv_orders(file: UploadFile):
    raw = await file.read()
    buf = io.StringIO(raw.decode("utf-8"))
    reader = csv.DictReader(buf)
    orders = []
    for r in reader:
        oid = str(r.get("pedido") or r.get("id") or "").strip()
        address = (r.get("endereco") or r.get("address") or "").strip()
        valor = float(r.get("valor") or r.get("value") or 0)
        earliest = (r.get("janela_inicio") or r.get("earliest") or None) or None
        latest   = (r.get("janela_fim") or r.get("latest") or None) or None

        lat, lng = geocode_address(address)
        orders.append(Order(
            id=oid if oid else address,
            pickup=None,
            dropoff=Location(lat=lat, lng=lng, address=address),
            value=valor,
            service_time_min=float(r.get("service_time_min") or 0),
            earliest=earliest,
            latest=latest,
            weight=float(r.get("weight") or 0),
        ))
    return orders
