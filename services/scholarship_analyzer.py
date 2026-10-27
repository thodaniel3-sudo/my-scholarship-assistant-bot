"""Scholarship link / text analysis.

MVP: fetches URL or accepts text, sends to AI for structured extraction,
returns a clean Telegram message. Extend the schema as you add features.
"""
import logging
import re
import httpx
from bs4 import BeautifulSoup
from services.ai_provider import chat
from utils.url_safety import is_safe_url

log = logging.getLogger(__name__)

PROMPT = """You are an academic scholarship analyst.
Extract the following fields from the user-provided scholarship text.
Return plain text, one field per line, using EXACTLY these labels.
If a field is not stated, write "Not stated in the available sources."

A. Scholarship name:
B. Funding organization:
C. Host country and university:
D. Degree levels:
E. Eligible nationalities:
F. Academic requirements:
G. English-language requirements:
H. Funding benefits:
I. Deadline:
J. Required documents:
K. Application procedure:
L. Official application portal:
M. Official information source:
N. Eligibility warnings:
O. Missing or unverified information:
P. Recommended next actions:
"""


async def _fetch_page(url: str) -> str:
    if not is_safe_url(url):
        return ""
    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=False) as client:
            r = await client.get(url)
            r.raise_for_status()
            html = r.text[:200_000]  # size cap
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return re.sub(r"\s+", " ", soup.get_text(" "))[:8000]
    except Exception as e:
        log.warning("Fetch failed for %s: %s", url, e)
        return ""


async def analyze_scholarship(input_text: str, user_id: int) -> str:
    input_text = input_text.strip()
    url = input_text if input_text.startswith("http") else ""
    body = ""
    if url:
        body = await _fetch_page(url)
        if not body:
            return ("Could not fetch that URL safely. "
                    "Please paste the scholarship text directly.")
        content_for_ai = body
    else:
        content_for_ai = input_text[:8000]

    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": content_for_ai},
    ]
    reply = await chat(messages, max_tokens=900)
    if not reply:
        return ("AI provider not configured. Set AI_API_KEY, AI_BASE_URL, AI_MODEL "
                "in .env. Meanwhile, here is the raw text length: "
                f"{len(content_for_ai)} chars.")
    header = f"Scholarship analysis\nSource: {url or 'pasted text'}\n\n"
    return (header + reply)[:4000]