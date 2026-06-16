# groq calls
import hashlib
import os
from groq import Groq

MODEL = "llama-3.3-70b-versatile"

_client = None
ai_cache = {}  # md5_hash -> summary string

SYSTEM_PROMPT = """You are a senior developer doing a quick code review pass.
Given a file from a software project, write exactly 3 sentences:
1. What this file's primary responsibility is
2. What it depends on or what depends on it
3. One thing a new developer should know before modifying it

No preamble. No "Sure, here's the summary". Just the 3 sentences."""


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_KEY"))
    return _client


def summarise(f_name, content):
    h = hashlib.md5(content.encode()).hexdigest()
    if h in ai_cache:
        return ai_cache[h]
    try:
        resp = _get_client().chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"File: {f_name}\n---\n{content[:6000]}"},
            ],
            temperature=0.3,
        )
        result = resp.choices[0].message.content.strip()
    except Exception:
        result = "Summary unavailable (rate limit or error). Try again in a moment."
    ai_cache[h] = result
    return result
