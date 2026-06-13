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

    tree = github_api.get_tree(gh_tok, owner, repo)
    blobs = [t for t in tree if utils.is_allowed(t["path"])]

    f_map = {}
    for item in blobs:
        path = item["path"]
        content = github_api.get_content(gh_tok, owner, repo, path)
        if content is not None:
            f_map[path] = content

    dep_g = parser.parse(f_map)
    return dep_g


@app.post("/summarise")
def summarise(body: dict):
    f_name = body.get("f_name", "")
    content = body.get("content", "")
    if not content:
        return {"summary": "No content provided."}
    return {"summary": ai_layer.summarise(f_name, content)}
