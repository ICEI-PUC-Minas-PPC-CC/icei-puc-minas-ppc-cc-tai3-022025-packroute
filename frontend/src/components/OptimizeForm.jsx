import { useState } from "react";
import { optimize } from "../api";

export default function OptimizeForm({ onResult }) {
  const [objective, setObjective] = useState("min_time");
  const [metric, setMetric] = useState("distance");
  const [returnDepot, setReturnDepot] = useState(true);
  const [loading, setLoading] = useState(false);

  async function run() {
    setLoading(true);
    try {
      const payload = {
        orders: [],   // opcional: popular do CSV no futuro
        vehicles: [], // opcional: do formulário
        objective, metric, return_to_depot: returnDepot
      };
      const res = await optimize(payload);
      onResult(res);
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div>
        <label>Objetivo:&nbsp;
          <select value={objective} onChange={e=>setObjective(e.target.value)}>
            <option value="min_time">Min tempo</option>
            <option value="min_distance">Min distância</option>
            <option value="max_profit">Max lucro</option>
          </select>
        </label>
      </div>
      <div>
        <label>Métrica:&nbsp;
          <select value={metric} onChange={e=>setMetric(e.target.value)}>
            <option value="distance">Distância</option>
            <option value="time">Tempo</option>
          </select>
        </label>
      </div>
      <div>
        <label><input type="checkbox" checked={returnDepot} onChange={e=>setReturnDepot(e.target.checked)} /> Voltar ao depósito</label>
      </div>
      <button onClick={run} disabled={loading}>{loading ? "Otimizando..." : "Otimizar"}</button>
    </div>
  );
}
