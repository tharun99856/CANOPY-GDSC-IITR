# helpers
import base64

ALLOWED = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"}


def b64_decode(b64_s):
    """Decode a base64 string to utf-8 text. Returns None on failure."""
    try:
        return base64.b64decode(b64_s).decode("utf-8")
    except Exception:
        return None


def is_allowed(path):
    """Check if a file path has a parseable extension."""
    for ext in ALLOWED:
        if path.endswith(ext):
            return True
        return False


def clean_path(path):
    """Return the path as-is — nodes use relative repo paths."""
    return path
