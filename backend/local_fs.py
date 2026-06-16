# read a local directory into a {path: content} map
import os
import utils

SKIP_DIRS = {"node_modules", ".git", "__pycache__", "dist", "build", ".venv", "venv"}


def read_dir(root, max_files=300):
    """Walk a local folder and return ({rel_path: content}, hit_cap)."""
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        raise FileNotFoundError(f"Not a directory: {root}")

    f_map = {}
    hit_cap = False
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/")
            if not utils.is_allowed(rel):
                continue
            if len(f_map) >= max_files:
                hit_cap = True
                break
            try:
                with open(os.path.join(dirpath, name), "r", encoding="utf-8") as fh:
                    f_map[rel] = fh.read()
            except (OSError, UnicodeDecodeError):
                continue
        if hit_cap:
            break

    return f_map, hit_cap
