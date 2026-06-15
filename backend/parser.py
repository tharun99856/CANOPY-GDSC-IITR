EXT_MAP = {
    ".py": "py",
    ".js": "js",
    ".ts": "ts",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".mjs": "js",
    ".cjs": "js",
}


def _ext_type(path):
    for ext, t in EXT_MAP.items():
        if path.endswith(ext):
            return t
    return "other"


def parse(f_map):
    nodes = []
    edges = []
    for path, content in f_map.items():
        loc_c = len(content.splitlines())
        nodes.append({"id": path, "loc": loc_c, "type": _ext_type(path)})
    return {"nodes": nodes, "edges": edges}
