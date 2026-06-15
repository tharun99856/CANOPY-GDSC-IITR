import { useState } from "react";
import { fetchRepos, loadRepo } from "./api";

export default function GithubConnect({ onGraphLoaded }) {
  const [gh_tok, setGh_tok] = useState("");
  const [repo_l, setRepo_l] = useState([]);
  const [sel_r, setSel_r] = useState(null);
  const [is_auth, setIs_auth] = useState(false);
  const [is_load, setIs_load] = useState(false);
  const [error, setError] = useState("");
  const [username, setUsername] = useState("");

  async function handleConnect() {
    setError("");
    if (!gh_tok.trim()) return;
    setIs_load(true);
    try {
      const repos = await fetchRepos(gh_tok.trim());
      if (Array.isArray(repos) && repos.length > 0) {
        setRepo_l(repos);
        setIs_auth(true);
        setUsername(repos[0].owner);
        setSel_r(null);
      } else if (Array.isArray(repos) && repos.length === 0) {
        setError("No repos found for this token.");
      } else {
        setError("Invalid token. Check your PAT has repo scope.");
      }
    } catch (e) {
      setError("Invalid token or network error. Check your PAT has repo scope.");
    }
    setIs_load(false);
  }

  async function handlePickRepo(repo) {
    setError("");
    setSel_r(repo);
    setIs_load(true);
    try {
      const data = await loadRepo(repo.owner, repo.name, gh_tok.trim());
      if (data.error) {
        setError(data.error);
        setIs_load(false);
        return;
      }
      onGraphLoaded(data, repo.owner, repo.name);
    } catch (e) {
      setError("Failed to load repo: " + e.message);
    }
    setIs_load(false);
  }

  return (
    <div className="gh-connect">
      <div className="gh-connect-label" style={{ fontSize: 12, color: "var(--text-secondary)", marginBottom: 2 }}>
        GitHub Personal Access Token
      </div>

      <input
        className="gh-input"
        type="password"
        placeholder="ghp_xxxxxxxxxxxx"
        value={gh_tok}
        onChange={(e) => setGh_tok(e.target.value)}
        disabled={is_auth}
        onKeyDown={(e) => e.key === "Enter" && handleConnect()}
      />

      {!is_auth ? (
        <button className="gh-connect-btn" onClick={handleConnect} disabled={is_load || !gh_tok.trim()}>
          {is_load ? "Connecting..." : "Connect"}
        </button>
      ) : (
        <div className="connected-badge">Connected as @{username}</div>
      )}

      {error && <div className="error-msg">{error}</div>}

      {is_auth && (
        <>
          <div className="repo-list-label" style={{ marginTop: 8 }}>Your Repositories</div>
          <div className="repo-list">
            {repo_l.length === 0 ? (
              <div className="repo-loading">No repos found.</div>
            ) : (
              repo_l.map((repo) => (
                <div
                  key={`${repo.owner}/${repo.name}`}
                  className={`repo-item ${sel_r?.name === repo.name && sel_r?.owner === repo.owner ? "active" : ""}`}
                  onClick={() => handlePickRepo(repo)}
                >
                  <div className="repo-name">{repo.name}</div>
                  {repo.description && <div className="repo-desc">{repo.description}</div>}
                </div>
              ))
            )}
          </div>
        </>
      )}

      {is_load && sel_r && (
        <div className="repo-loading">Loading {sel_r.name}...</div>
      )}
    </div>
  );
}
