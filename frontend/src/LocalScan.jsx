import { useState, useRef, useEffect } from "react";
import { loadFiles } from "./api";

const ALLOWED = [".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"];
const SKIP = ["node_modules/", "/.git/", "__pycache__/", "dist/", "build/", ".venv/", "venv/"];

export default function LocalScan({ onGraphLoaded }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  // webkitdirectory has to be set as an attribute, not a React prop
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.setAttribute("webkitdirectory", "");
      inputRef.current.setAttribute("directory", "");
    }
  }, []);

  async function handlePick(e) {
    setError("");
    const all = Array.from(e.target.files || []);
    if (all.length === 0) return;

    setLoading(true);
    try {
      const picked = all.filter((f) => {
        const p = "/" + (f.webkitRelativePath || f.name);
        if (SKIP.some((s) => p.includes(s))) return false;
        return ALLOWED.some((ext) => p.endsWith(ext));
      });

      if (picked.length === 0) {
        setError("No parseable code files in that folder.");
        setLoading(false);
        return;
      }
      if (picked.length > 300) {
        setError(`That folder has ${picked.length} code files (max 300). Try a smaller one.`);
        setLoading(false);
        return;
      }

      const rootName = (all[0].webkitRelativePath || "folder").split("/")[0];
      const files = {};
      for (const f of picked) {
        const rel = (f.webkitRelativePath || f.name).split("/").slice(1).join("/") || f.name;
        files[rel] = await f.text();
      }

      const data = await loadFiles(files);
      onGraphLoaded(data, "local", rootName);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="gh-connect local-scan">
      <div className="gh-connect-label" style={{ fontSize: 12, color: "var(--text-secondary)", marginBottom: 2 }}>
        Or scan a local folder
      </div>

      <input ref={inputRef} type="file" multiple style={{ display: "none" }} onChange={handlePick} />

      <button className="gh-connect-btn" onClick={() => inputRef.current?.click()} disabled={loading}>
        {loading ? "Scanning..." : "Choose folder"}
      </button>

      <div className="scan-hint">
        Pick a folder on your computer — Canopy reads the code files in your
        browser and maps them. Only the file text is sent for analysis.
      </div>

      {error && <div className="error-msg">{error}</div>}
    </div>
  );
}
