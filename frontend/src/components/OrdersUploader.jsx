import { useState } from "react";
import { uploadOrdersCsv } from "../api";

export default function OrdersUploader({ onUploaded }) {
  const [count, setCount] = useState(null);
  const [loading, setLoading] = useState(false);
  async function handleFile(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      const r = await uploadOrdersCsv(file);
      setCount(r.count);
      onUploaded?.(r);
    } catch (e) {
      alert(e.message);
    } finally {
      setLoading(false);
    }
  }
  return (
    <div>
      <label>CSV de pedidos: <input type="file" accept=".csv" onChange={handleFile} /></label>
      {loading && <p>Carregando…</p>}
      {count !== null && <p>{count} pedidos importados</p>}
    </div>
  );
}
