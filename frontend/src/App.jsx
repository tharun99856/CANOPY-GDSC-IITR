import { useState, useRef, useCallback } from "react";
import GithubConnect from "./GithubConnect";
import GraphCanvas from "./GraphCanvas";
import SidePanel from "./SidePanel";
import SearchBar from "./SearchBar";
import LocalScan from "./LocalScan";

function App() {
  const [g_data, setG_data] = useState(null);
  const [sel_n, setSel_n] = useState(null);
  const [search_q, setSearch_q] = useState("");
  const [repo_name, setRepo_name] = useState("");
  const [repo_owner, setRepo_owner] = useState("");

  const handleGraphLoaded = useCallback((data, owner, name) => {
    setG_data(data);
    setRepo_owner(owner);
    setRepo_name(name);
    setSel_n(null);
    setSearch_q("");
  }, []);

  const handleNodeClick = useCallback((node) => {
    setSel_n((prev) => (prev?.id === node.id ? null : node));
  }, []);

  return (
    <div className="app-shell">
      <div className="topbar">
        <span className="logo">Canopy</span>
        {repo_name && (
          <span style={{ fontSize: 12, color: "var(--text-secondary)" }}>
            {repo_owner}/{repo_name}
          </span>
        )}
      </div>

      <div className="sidebar">
        <GithubConnect onGraphLoaded={handleGraphLoaded} />
        <LocalScan onGraphLoaded={handleGraphLoaded} />
      </div>

      <div className="canvas-area">
        {g_data ? (
          <>
            <SearchBar value={search_q} onChange={setSearch_q} />
            <GraphCanvas
              g_data={g_data}
              sel_n={sel_n}
              search_q={search_q}
              onNodeClick={handleNodeClick}
            />
          </>
        ) : (
          <div className="empty-state">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="1.5">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
            <h1 className="entry-title">Canopy</h1>
            <p className="entry-headline">See your codebase from above.</p>
            <span>Connect to GitHub or scan a local folder to begin</span>
          </div>
        )}
      </div>

      <div className="side-panel">
        {g_data && sel_n ? (
          <SidePanel node={sel_n} g_data={g_data} />
        ) : (
          <div className="side-panel-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--border)" strokeWidth="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4M12 8h.01"/>
            </svg>
            <span>Click a file node to see its AI summary</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
