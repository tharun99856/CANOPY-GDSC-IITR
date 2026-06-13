const BASE = import.meta.env.VITE_BACKEND || "http://localhost:8000";

export async function fetchRepos(token) {
  const r = await fetch(`${BASE}/repos?token=${encodeURIComponent(token)}`);
  if (!r.ok) throw new Error("Failed to fetch repos");
  const data = await r.json();
  if (data.error) throw new Error(data.error);
  return data;
}

export async function loadRepo(owner, repo, token) {
  const r = await fetch(`${BASE}/load-repo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ owner, repo, token }),
  });
  if (!r.ok) throw new Error("Failed to load repo");
  const data = await r.json();
  if (data.error) throw new Error(data.error);
  return data;
}

export async function fetchSummary(f_name, content) {
  const r = await fetch(`${BASE}/summarise`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ f_name, content }),
  });
  if (!r.ok) throw new Error("Failed to fetch summary");
  const data = await r.json();
  return data.summary;
}
