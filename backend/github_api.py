# github api calls
import httpx

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
    """Get recursive file tree. TODO: real API call."""
    return []


def get_content(gh_tok, owner, repo, path):
    """Fetch and decode file content. TODO: real API call."""
    return None
