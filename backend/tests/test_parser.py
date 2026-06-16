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


def _edges(graph):
    return {(e["src"], e["tgt"]) for e in graph["edges"]}


def test_python_import_resolves_to_edge():
    graph = parser.parse({"main.py": "import helper\n", "helper.py": "x = 1\n"})
    assert ("main.py", "helper.py") in _edges(graph)


def test_js_relative_import_resolves_to_edge():
    graph = parser.parse({
        "src/App.jsx": "import Foo from './Foo'\n",
        "src/Foo.jsx": "export default 1\n",
    })
    assert ("src/App.jsx", "src/Foo.jsx") in _edges(graph)


def test_bare_package_import_is_ignored():
    graph = parser.parse({"src/App.jsx": "import React from 'react'\n"})
    assert graph["edges"] == []
