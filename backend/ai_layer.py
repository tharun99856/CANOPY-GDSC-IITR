# gemini calls
import hashlib
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

ai_cache = {}  # md5_hash -> summary string

PROMPT = """You are a senior developer doing a quick code review pass.
Given the file below from a software project, write exactly 3 sentences:
1. What this file's primary responsibility is
2. What it depends on or what depends on it
3. One thing a new developer should know before modifying it

No preamble. No "Sure, here's the summary". Just the 3 sentences.

File: {f_name}
---
{content}"""


def summarise(f_name, content):
    h = hashlib.md5(content.encode()).hexdigest()
    if h in ai_cache:
        return ai_cache[h]
    try:
        resp = model.generate_content(
            PROMPT.format(f_name=f_name, content=content[:6000])
        )
        result = resp.text.strip()
    except Exception:
        result = "Summary unavailable (rate limit or error). Try again in a moment."
    ai_cache[h] = result
    return result
