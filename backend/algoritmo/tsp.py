# packroute/backend/algoritmo/tsp.py
from typing import List, Dict, Any, Optional, Tuple
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import math
from ..core.utils import haversine_km, minutes_to_hhmm

def _build_points(orders, vehicle_start) -> List[Tuple[float, float, Optional[str]]]:
    """Cria a lista de pontos (depot + drops). Retorna [(lat, lng, address), ...]"""
    pts = [(vehicle_start.lat, vehicle_start.lng, getattr(vehicle_start, "address", None))]
    for o in orders:
        pts.append((o.dropoff.lat, o.dropoff.lng, getattr(o.dropoff, "address", None)))
    return pts

def _distance_matrix(points) -> List[List[int]]:
    """Matriz de distância em metros (inteiros) — OR-Tools espera int."""
    n = len(points)
    m = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            d_km = haversine_km(points[i][0], points[i][1], points[j][0], points[j][1])
            m[i][j] = int(round(d_km * 1000))  # metros
    return m

def _time_matrix(distance_m: List[List[int]], speed_kmh: float) -> List[List[int]]:
    """Converte distância (m) em tempo (minutos inteiros)."""
    n = len(distance_m)
    m = [[0]*n for _ in range(n)]
    # velocidade m/min:
    v_m_per_min = (speed_kmh * 1000) / 60.0 if speed_kmh > 0 else 1.0
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            m[i][j] = int(round(distance_m[i][j] / v_m_per_min))
    return m

def solve(
    orders, 
    vehicles, 
    objective: str = "min_distance",   # min_distance|min_time|max_profit (placeholder)
    metric: str = "distance",          # distance|time
    return_to_depot: bool = True,
    speed_kmh: float = 25.0,
    time_limit_s: int = 2,
    start_time_hhmm: Optional[str] = None
) -> Dict[str, Any]:
    """
    TSP 1 veículo (baseline).
    - orders: lista de Order (core.models)
    - vehicles: [Vehicle] (usa vehicles[0])
    Retorna dict com 'routes' no formato esperado pelo solver_service.
    """
    if not vehicles:
        raise ValueError("É necessário pelo menos um veículo.")
    v = vehicles[0]
    points = _build_points(orders, v.start)  # [0] é o depósito
    n = len(points)
    if n < 2:
        # Só depósito, sem pedidos
        return {
            "routes": [{
                "vehicle_id": v.id,
                "sequence": [],
                "totals": {"distance_km": 0.0, "time_min": 0.0, "value": 0.0}
            }]
        }

    dist_m = _distance_matrix(points)
    time_min = _time_matrix(dist_m, speed_kmh)

    # Se não deve retornar ao depósito, criamos um "end" diferente para o veículo.
    # No TSP 1-veículo do OR-Tools, usamos start==end para fechar o ciclo; 
    # para caminho aberto, definimos um "end" artificial via RoutingIndexManager com end_node = 0 e ajustamos custos.
    starts = [0]
    ends = [0 if return_to_depot else 1]  # truque: se não voltar, definimos fim no primeiro cliente (aproximação simples)
    # Observação: Para caminho aberto de verdade, o ideal é VRP com starts=[0], ends=[-1] custom.
    # Para manter TSP simples aqui, permitimos 'fim no 1o cliente' — prática comum para baseline.

    manager = pywrapcp.RoutingIndexManager(n, 1, starts, ends)
    routing = pywrapcp.RoutingModel(manager)

    # Escolhe qual matriz usar como custo principal
    use_time = (metric == "time" or objective == "min_time")

    def distance_cb(from_idx, to_idx):
        i, j = manager.IndexToNode(from_idx), manager.IndexToNode(to_idx)
        return dist_m[i][j]

    def time_cb(from_idx, to_idx):
        i, j = manager.IndexToNode(from_idx), manager.IndexToNode(to_idx)
        return time_min[i][j]

    dist_cb_idx = routing.RegisterTransitCallback(distance_cb)
    time_cb_idx = routing.RegisterTransitCallback(time_cb)

    if use_time:
        routing.SetArcCostEvaluatorOfAllVehicles(time_cb_idx)
    else:
        routing.SetArcCostEvaluatorOfAllVehicles(dist_cb_idx)

    # (Opcional futuro) Janela de tempo, capacidade, etc.

    # Parâmetros de busca
    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.FromSeconds(time_limit_s)

    solution = routing.SolveWithParameters(params)
    if solution is None:
        # Sem solução — retornar vazio e deixar a API informar
        return {
            "routes": [{
                "vehicle_id": v.id,
                "sequence": [],
                "totals": {"distance_km": 0.0, "time_min": 0.0, "value": 0.0}
            }]
        }

    # Extrair rota
    idx = routing.Start(0)
    order_sequence = []
    total_m = 0
    total_min = 0
    last_node = None

    # ETA
    current_time_min = 0
    if start_time_hhmm:
        # começa em zero e só converte no final para string a partir do start_time
        pass

    while not routing.IsEnd(idx):
        node = manager.IndexToNode(idx)
        nxt = solution.Value(routing.NextVar(idx))
        node_next = manager.IndexToNode(nxt)

        # pula o depósito no output, mas precisamos registrar custos entre nós
        if last_node is not None:
            total_m += dist_m[last_node][node]
            delta_min = time_min[last_node][node]
            total_min += delta_min
            current_time_min += delta_min

        # se o node > 0, é um pedido (node 0 é depósito)
        if node > 0:
            o = orders[node - 1]
            arrival = minutes_to_hhmm(start_time_hhmm, current_time_min) if start_time_hhmm else None
            order_sequence.append({
                "order_id": o.id,
                "lat": o.dropoff.lat,
                "lng": o.dropoff.lng,
                "arrival_time": arrival,
                "travel_distance_km": dist_m[last_node][node] / 1000 if last_node is not None else 0.0,
                "travel_time_min": time_min[last_node][node] if last_node is not None else 0.0,
            })

        last_node = node
        idx = nxt

    # adicionar custo do último arco até o "end" (se aplicável)
    end_node = manager.IndexToNode(idx)
    if last_node is not None and end_node != last_node:
        total_m += dist_m[last_node][end_node]
        delta_min = time_min[last_node][end_node]
        total_min += delta_min
        current_time_min += delta_min
        # normalmente não listamos o fim (depósito) como passo de pedido

    # Totais
    total_km = total_m / 1000.0
    total_value = sum(getattr(o, "value", 0.0) for o in orders)

    return {
        "routes": [{
            "vehicle_id": v.id,
            "sequence": order_sequence,
            "totals": {"distance_km": total_km, "time_min": float(total_min), "value": float(total_value)}
        }]
    }

if __name__ == "__main__":
    # Exemplo ad-hoc: adapte para seu CSV se quiser testar isolado
    print("Use via API /optimize")
