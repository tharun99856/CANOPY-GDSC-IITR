import re

PY_RE = re.compile(r'^\s*(?:import|from)\s+([\w.]+)')
JS_RE = re.compile(r'''(?:from\s+|import\s+|require\s*\(\s*)['"]([^'"]+)['"]''')

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


def _normalize(path):
    parts = path.replace("\\", "/").split("/")
    out = []
    for p in parts:
        if p == ".":
            continue
        elif p == ".." and out:
            out.pop()
        else:
            out.append(p)
    return "/".join(out)


def _resolve_py(src_path, module, all_paths):
    src_dir = src_path.rsplit("/", 1)[0] if "/" in src_path else ""
    module_path = module.replace(".", "/")

    candidates = []
    if src_dir:
        candidates.append(f"{src_dir}/{module_path}.py")
        candidates.append(f"{src_dir}/{module_path}/__init__.py")
    candidates.append(f"{module_path}.py")
    candidates.append(f"{module_path}/__init__.py")

    for c in candidates:
        n = _normalize(c)
        if n in all_paths:
            return n
    return None


def _resolve_js(src_path, imp, all_paths):
    if not imp.startswith("."):
        return None

    src_dir = src_path.rsplit("/", 1)[0] if "/" in src_path else ""
    base = _normalize(f"{src_dir}/{imp}" if src_dir else imp)

    for ext in ("", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"):
        if (base + ext) in all_paths:
            return base + ext

    for idx in ("/index.js", "/index.ts", "/index.tsx", "/index.jsx"):
        if (base + idx) in all_paths:
            return base + idx

    return None


def parse(f_map):
    all_paths = set(f_map.keys())
    nodes = []
    edges = []
    seen = set()

    for path, content in f_map.items():
        loc_c = len(content.splitlines())
        nodes.append({"id": path, "loc": loc_c, "type": _ext_type(path)})

        if path.endswith(".py"):
            for line in content.splitlines():
                m = PY_RE.match(line)
                if m:
                    tgt = _resolve_py(path, m.group(1), all_paths)
                    if tgt and tgt != path and (path, tgt) not in seen:
                        seen.add((path, tgt))
                        edges.append({"src": path, "tgt": tgt})

        elif any(path.endswith(e) for e in (".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs")):
            for line in content.splitlines():
                for m in JS_RE.finditer(line):
                    tgt = _resolve_js(path, m.group(1), all_paths)
                    if tgt and tgt != path and (path, tgt) not in seen:
                        seen.add((path, tgt))
                        edges.append({"src": path, "tgt": tgt})

    return {"nodes": nodes, "edges": edges}
