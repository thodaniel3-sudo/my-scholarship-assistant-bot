"""Safe, registry-driven search over Supabase."""
import logging
from database.supabase_client import get_client
from database.table_registry import SEARCHABLE_TABLES

log = logging.getLogger(__name__)


def search_table(table: str, query: str, limit: int = 5) -> list[dict]:
    cfg = SEARCHABLE_TABLES.get(table)
    if not cfg:
        return []
    cols = cfg.get("search_columns") or []
    if not cols:
        return []
    select_cols = ",".join(cfg["return_columns"])
    try:
        q = get_client().table(table).select(select_cols).limit(limit)
        # OR across search columns using ilike
        or_expr = ",".join(f"{c}.ilike.%{query}%" for c in cols)
        q = q.or_(or_expr)
        return q.execute().data or []
    except Exception as e:
        log.error("Search failed on %s: %s", table, e)
        return []