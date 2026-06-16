import { useState } from "react";
import { loadLocal } from "./api";

export default function LocalScan({ onGraphLoaded }) {
  const [path, setPath] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleScan() {
    setError("");
    if (!path.trim()) return;
    setLoading(true);
    try {
      const data = await loadLocal(path.trim());
      const name = path.trim().replace(/[\\/]+$/, "").split(/[\\/]/).pop() || "folder";
      onGraphLoaded(data, "local", name);
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  }

  return (
    <div className="gh-connect local-scan">
      <div className="gh-connect-label" style={{ fontSize: 12, color: "var(--text-secondary)", marginBottom: 2 }}>
        Or scan a local folder
      </div>

      <input
        className="gh-input"
        type="text"
        placeholder="C:\path\to\project"
        value={path}
        onChange={(e) => setPath(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleScan()}
      />

      <button className="gh-connect-btn" onClick={handleScan} disabled={loading || !path.trim()}>
        {loading ? "Scanning..." : "Scan folder"}
      </button>

      <div className="scan-hint">
        Only works when you run Canopy on your own machine — then it can read
        folders from your computer.
      </div>

      {error && <div className="error-msg">{error}</div>}
    </div>
  );
}
