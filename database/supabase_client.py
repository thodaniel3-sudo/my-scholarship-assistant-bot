"""Supabase client (server-side only)."""
import logging
from supabase import create_client, Client
from config import settings

log = logging.getLogger(__name__)
_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_secret_key)
    return _client


def check_health() -> bool:
    try:
        get_client().table("universities").select("id").limit(1).execute()
        return True
    except Exception as e:
        log.error("Supabase health check failed: %s", e)
        return False