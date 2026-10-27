"""Very simple intent router.

Right now it sends every query to Brave Search and (optionally) the AI.
Extend the branches as you enable more features.
"""
import logging
from services.brave_search import search_web
from services.ai_provider import summarize_results

log = logging.getLogger(__name__)


async def route_text(text: str, user_id: int) -> str:
    text = text.strip()
    if not text:
        return "Please send a question."

    if text.lower().startswith("show my saved"):
        return "You have no saved items yet (feature to be wired to user tables)."

    if text.lower().startswith("show my saved deadlines"):
        return "No upcoming deadlines on file yet."

    # Default: Brave Search + optional AI summary
    results = await search_web(text, count=5)
    if not results:
        return ("No web results found. Check that BRAVE_SEARCH_API_KEY is set "
                "or try a different query.")

    summary = await summarize_results(text, results)
    lines = [summary, ""]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}\n{r['url']}\n{r.get('description','')[:200]}")
    return "\n\n".join(lines)[:4000]