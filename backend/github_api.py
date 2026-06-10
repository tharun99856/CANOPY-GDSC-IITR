# github api calls — stub for now, real implementation in a later pass

BASE = "https://api.github.com"


def list_repos(gh_tok):
    """List repos for the authenticated user. TODO: real API call."""
    return []


def get_tree(gh_tok, owner, repo):
    """Get recursive file tree. TODO: real API call."""
    return []


def get_content(gh_tok, owner, repo, path):
    """Fetch and decode file content. TODO: real API call."""
    return None
