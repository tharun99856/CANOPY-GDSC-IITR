# groq calls
import hashlib
import os
from groq import Groq

MODEL = "llama-3.3-70b-versatile"

_client = None
ai_cache = {}

SYSTEM_PROMPT = """You are a senior developer doing a quick code review pass.
Given a file from a software project and its dependency context, write exactly 3 sentences:
1. What this file's primary responsibility is
2. How it fits into the project based on the dependency info provided
3. One thing a new developer should know before modifying it

No preamble. Just the 3 sentences."""


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_KEY"))
    return _client


def summarise(f_name, content, imports=None, imported_by=None):
    h = hashlib.md5(content.encode()).hexdigest()
    if h in ai_cache:
        return ai_cache[h]

    ctx = f"File: {f_name}\n"
    if imports:
        ctx += f"This file imports: {', '.join(imports)}\n"
    if imported_by:
        ctx += f"Imported by: {', '.join(imported_by)}\n"
    ctx += f"---\n{content[:6000]}"

    try:
        resp = _get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": ctx},
            ],
            temperature=0.2,
        )
        result = resp.choices[0].message.content.strip()
    except Exception:
        result = "Summary unavailable (rate limit or error). Try again in a moment."
    ai_cache[h] = result
    return result
