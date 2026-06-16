from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import github_api
import parser
import ai_layer
import utils

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/repos")
def repos(token: str):
    try:
        return github_api.list_repos(token)
    except Exception as e:
        return {"error": str(e)}


@app.post("/load-repo")
def load_repo(body: dict):
    gh_tok = body.get("token")
    owner = body.get("owner")
    repo = body.get("repo")
    max_files = body.get("max_files", 300)

    try:
        tree = github_api.get_tree(gh_tok, owner, repo)
    except Exception as e:
        return {"error": f"Failed to fetch tree: {e}"}

    # Filter to parseable files only
    blobs = [t for t in tree if utils.is_allowed(t["path"])]

    if len(blobs) > max_files:
        return {
            "error": f"Repo has {len(blobs)} parseable files (cap is {max_files}). "
            "This tool works best with repos under 300 files."
        }

    f_map = {}
    for item in blobs:
        path = item["path"]
        content = github_api.get_content(gh_tok, owner, repo, path)
        if content is not None:
            f_map[path] = content

    if not f_map:
        return {"error": "No parseable files found in this repo."}

    dep_g = parser.parse(f_map)
    # Include raw content for the AI summary layer
    dep_g["_content"] = {k: v[:6000] for k, v in f_map.items()}
    return dep_g


@app.post("/summarise")
def summarise(body: dict):
    f_name = body.get("f_name", "")
    content = body.get("content", "")
    if not content:
        return {"summary": "No content provided."}
    return {"summary": ai_layer.summarise(f_name, content)}
