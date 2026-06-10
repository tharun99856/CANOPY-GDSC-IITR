# dependency graph parser — stub for now

def parse(f_map):
    """Build a dependency graph from {path: content}. TODO: real parsing."""
    nodes = []
    edges = []
    for path in f_map:
        nodes.append({"id": path, "loc": 0, "type": "other"})
    return {"nodes": nodes, "edges": edges}
