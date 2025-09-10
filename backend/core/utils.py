# packroute/backend/core/utils.py
import math, hashlib, os
from functools import lru_cache
from typing import Optional

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def pad2(n: int) -> str: return str(n).rjust(2, "0")

def minutes_to_hhmm(start_hhmm: Optional[str], delta_min: int) -> Optional[str]:
    if start_hhmm is None: return None
    h0, m0 = [int(x) for x in start_hhmm.split(":")]
    total = (h0 * 60 + m0 + int(round(delta_min))) % (24*60)
    return f"{pad2(total//60)}:{pad2(total%60)}"

# === Geocoder stub (determinístico) ===
# Gera coordenadas falsas ao redor de um centro (default: centro de SP)
CENTER_LAT = float(os.getenv("PACKROUTE_FAKE_GEOCODER_CENTER_LAT", "-23.550520"))
CENTER_LNG = float(os.getenv("PACKROUTE_FAKE_GEOCODER_CENTER_LNG", "-46.633308"))
RADIUS_KM   = float(os.getenv("PACKROUTE_FAKE_GEOCODER_RADIUS_KM", "5.0"))  # raio onde “espalhamos” pontos

@lru_cache(maxsize=1024)
def geocode_address(address: str) -> tuple[float, float]:
    """
    Geocodifica 'address' de forma determinística (sem chamadas externas).
    Distribui em um círculo ao redor do centro definido por env.
    """
    if not address:
        return (CENTER_LAT, CENTER_LNG)
    # cria ângulo e raio pseudo-aleatórios baseados no hash do endereço
    h = hashlib.sha256(address.encode("utf-8")).hexdigest()
    ang = int(h[:8], 16) / 0xFFFFFFFF * 2 * math.pi
    r01 = int(h[8:16], 16) / 0xFFFFFFFF
    r_km = (0.2 + 0.8 * r01) * RADIUS_KM  # entre 0.2R e R
    # desloca em metros aproximando 1 deg lat ~ 111km e lon ~ 111km*cos(lat)
    dlat = (r_km / 111.0) * math.sin(ang)
    dlng = (r_km / (111.0 * math.cos(math.radians(CENTER_LAT)))) * math.cos(ang)
    return (CENTER_LAT + dlat, CENTER_LNG + dlng)
