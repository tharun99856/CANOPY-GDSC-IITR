# github api calls
import httpx
import utils

BASE = "https://api.github.com"
HEAD = lambda tok: {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"}


def list_repos(gh_tok):
    """List repos for the authenticated user. Returns [{name, owner, description, updated_at}]."""
    r = httpx.get(
        f"{BASE}/user/repos?per_page=100&sort=updated",
        headers=HEAD(gh_tok),
        timeout=30.0,
    )
    r.raise_for_status()
    data = r.json()
    return [
        {
            "name": d["name"],
            "owner": d["owner"]["login"],
            "description": d.get("description") or "",
            "updated_at": d.get("updated_at") or "",
        }
        for d in data
    ]


def get_tree(gh_tok, owner, repo):
    """Get recursive file tree. Returns list of {path, type} blobs only."""
    r = httpx.get(
        f"{BASE}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1",
        headers=HEAD(gh_tok),
        timeout=60.0,
    )
    r.raise_for_status()
    data = r.json()
    tree = data.get("tree", [])
    return [{"path": t["path"], "type": t["type"]} for t in tree if t["type"] == "blob"]


def get_content(gh_tok, owner, repo, path):
    """Fetch and decode file content. Returns utf-8 string or None."""
    r = httpx.get(
        f"{BASE}/repos/{owner}/{repo}/contents/{path}",
        headers=HEAD(gh_tok),
        timeout=30.0,
    )
    if r.status_code == 404:
        return None
    r.raise_for_status()
    data = r.json()
    b64_c = data.get("content", "")
    if not b64_c:
        return None
    return utils.b64_decode(b64_c)
