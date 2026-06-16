# helpers
import base64

ALLOWED = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"}


def b64_decode(b64_s):
    try:
        return base64.b64decode(b64_s).decode("utf-8")
    except Exception:
        return None


def is_allowed(path):
    for ext in ALLOWED:
        if path.endswith(ext):
            return True
    return False


def clean_path(path):
    """Return the path as-is — nodes use relative repo paths."""
    return path
