from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .core.schemas import OptimizeRequest, OptimizeResponse
from .services.solver_service import solve_tsp_or_vrp
from .services.parsers import parse_csv_orders

app = FastAPI(title="PackRoute API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest):
    try:
        result = solve_tsp_or_vrp(req)
        return {
            "routes": [
                {
                    "vehicle_id": r["vehicle_id"],
                    "sequence": r["sequence"],
                    "total_distance_km": r["totals"]["distance_km"],
                    "total_time_min": r["totals"]["time_min"],
                    "total_value": r["totals"]["value"],
                }
                for r in result["routes"]
            ],
            "objective": req.objective,
            "metric": req.metric,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders/upload_csv", response_model=dict)
async def upload_orders(file: UploadFile = File(...)):
    orders = await parse_csv_orders(file)
    return {"count": len(orders)}
