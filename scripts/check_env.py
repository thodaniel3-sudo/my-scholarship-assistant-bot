"""Quick sanity check of .env before running the bot."""
from config import settings

print("TELEGRAM_BOT_TOKEN set:", bool(settings.telegram_bot_token))
print("SUPABASE_URL set:", bool(settings.supabase_url))
print("SUPABASE_SECRET_KEY set:", bool(settings.supabase_secret_key))
print("BRAVE_SEARCH_API_KEY set:", bool(settings.brave_search_api_key))
print("AI_API_KEY set:", bool(settings.ai_api_key))
print("Admin IDs:", settings.admin_ids)