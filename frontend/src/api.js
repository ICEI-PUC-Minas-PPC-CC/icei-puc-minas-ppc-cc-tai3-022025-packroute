const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function optimize(payload) {
  const res = await fetch(`${API_URL}/optimize`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Erro na otimização");
  return res.json();
}

export async function uploadOrdersCsv(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/orders/upload_csv`, { method: "POST", body: form });
  if (!res.ok) throw new Error("Falha no upload");
  return res.json();
}
