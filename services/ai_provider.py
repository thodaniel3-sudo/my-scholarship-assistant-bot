"""Provider-agnostic AI wrapper (OpenAI-compatible chat completions)."""
import logging
import httpx
from config import settings

log = logging.getLogger(__name__)


async def chat(messages: list[dict], max_tokens: int = 500) -> str:
    if not settings.ai_api_key:
        return ""
    url = f"{settings.ai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.ai_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error("AI call failed: %s", e)
        return ""


async def summarize_results(query: str, results: list[dict]) -> str:
    if not results:
        return ""
    bullet = "\n".join(f"- {r['title']}: {r.get('description','')[:200]}" for r in results[:5])
    messages = [
        {"role": "system", "content": "You are an academic research assistant. "
                                      "Summarise the provided search results in 3-5 short sentences. "
                                      "Do not invent facts not present in the results."},
        {"role": "user", "content": f"Query: {query}\n\nResults:\n{bullet}"},
    ]
    out = await chat(messages, max_tokens=300)
    return out or "Top results below:"