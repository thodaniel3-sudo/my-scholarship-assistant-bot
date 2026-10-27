"""Brave Search API wrapper.

Docs: https://api.search.brave.com/app/documentation/web-search/get-started
"""
import logging
import httpx
from config import settings

log = logging.getLogger(__name__)
BRAVE_URL = "https://api.search.brave.com/res/v1/web/search"


def check_health() -> bool:
    return bool(settings.brave_search_api_key)


async def search_web(query: str, count: int = 5, country: str = "us") -> list[dict]:
    if not settings.brave_search_api_key:
        log.warning("BRAVE_SEARCH_API_KEY missing; returning empty results.")
        return []

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": settings.brave_search_api_key,
    }
    params = {"q": query, "count": min(count, 20), "country": country}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.get(BRAVE_URL, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        log.error("Brave search failed: %s", e)
        return []

    out = []
    for item in data.get("web", {}).get("results", []):
        out.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
        })
    return out