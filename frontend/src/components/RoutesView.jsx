export default function RoutesView({ data }) {
  if (!data) return null;
  return (
    <div>
      {data.routes.map(r => (
        <div key={r.vehicle_id} style={{border:"1px solid #ddd", borderRadius:8, padding:12, marginBottom:12}}>
          <h3>Veículo {r.vehicle_id}</h3>
          <p><b>Total:</b> {r.total_distance_km.toFixed(2)} km • {r.total_time_min.toFixed(0)} min • R$ {r.total_value.toFixed(2)}</p>
          <ol>
            {r.sequence.map((s, idx) => (
              <li key={idx}>
                {s.order_id ? `Pedido ${s.order_id}` : "Início/Fim"} — {s.travel_distance_km.toFixed(2)} km, {s.travel_time_min.toFixed(0)} min {s.arrival_time ? `• ETA ${s.arrival_time}` : ""}
              </li>
            ))}
          </ol>
        </div>
      ))}
    </div>
  );
}
