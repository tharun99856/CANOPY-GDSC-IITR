import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import parser


def _nodes_by_id(graph):
    return {n["id"]: n for n in graph["nodes"]}


def test_file_typing():
    graph = parser.parse({"a.py": "", "b.tsx": "", "c.js": "", "d.txt": ""})
    nodes = _nodes_by_id(graph)
    assert nodes["a.py"]["type"] == "py"
    assert nodes["b.tsx"]["type"] == "tsx"
    assert nodes["c.js"]["type"] == "js"
    assert nodes["d.txt"]["type"] == "other"


def test_line_of_code_count():
    graph = parser.parse({"a.py": "x = 1\ny = 2\nz = 3\n"})
    nodes = _nodes_by_id(graph)
    assert nodes["a.py"]["loc"] == 3
