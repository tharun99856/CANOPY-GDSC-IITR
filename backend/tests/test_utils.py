import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import utils


def test_is_allowed_accepts_known_extensions():
    assert utils.is_allowed("src/app.py")
    assert utils.is_allowed("a/b/Component.tsx")
    assert utils.is_allowed("index.mjs")


def test_is_allowed_rejects_other_extensions():
    assert not utils.is_allowed("README.md")
    assert not utils.is_allowed("logo.png")
    assert not utils.is_allowed("Makefile")


def test_b64_decode_roundtrip():
    encoded = base64.b64encode("hello world".encode()).decode()
    assert utils.b64_decode(encoded) == "hello world"


def test_b64_decode_returns_none_on_invalid_utf8():
    encoded = base64.b64encode(b"\xff\xfe").decode()
    assert utils.b64_decode(encoded) is None
