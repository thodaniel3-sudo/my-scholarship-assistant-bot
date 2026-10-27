"""Telegram command handlers and free-text router."""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from config import settings
from bot.router import route_text
from database.supabase_client import check_health as db_health
from services.brave_search import check_health as brave_health

log = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome to your Scholarship & Research Assistant.\n\n"
        "You can talk to me in plain English. Try:\n"
        "• Find master\u2019s programmes in materials science in Germany\n"
        "• Scholarships for Nigerian students\n"
        "• Research on natural-fibre composites\n\n"
        "Type /help to see all commands."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n"
        "/search <query> \u2014 general search\n"
        "/universities <query>\n"
        "/programmes <query>\n"
        "/scholarship <url or text>\n"
        "/research <query>\n"
        "/deadlines \u2014 upcoming saved deadlines\n"
        "/saved \u2014 your saved items\n"
        "/status \u2014 system health\n"
        "/help \u2014 this message\n\n"
        "Or just type any question."
    )


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db_ok = db_health()
    brave_ok = brave_health()
    await update.message.reply_text(
        f"System status:\n• Supabase: {'\u2705 OK' if db_ok else '\u274c down'}\n"
        f"• Brave Search key: {'\u2705 present' if brave_ok else '\u26a0\ufe0f missing'}\n"
        f"• AI key: {'\u2705 present' if bool(settings.ai_api_key) else '\u26a0\ufe0f missing'}"
    )


async def _plain(update: Update, text: str) -> None:
    await update.message.reply_text(text)


async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    if not query:
        await _plain(update, "Usage: /search <your query>")
        return
    reply = await route_text(query, update.effective_user.id)
    await _plain(update, reply)


async def universities_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip() or "all universities"
    reply = await route_text(f"universities: {query}", update.effective_user.id)
    await _plain(update, reply)


async def programmes_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip() or "all programmes"
    reply = await route_text(f"programmes: {query}", update.effective_user.id)
    await _plain(update, reply)


async def scholarships_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args).strip()
    if not text:
        await _plain(update, "Send a scholarship URL or paste the scholarship text after /scholarship.")
        return
    from services.scholarship_analyzer import analyze_scholarship
    reply = await analyze_scholarship(text, update.effective_user.id)
    await _plain(update, reply)


async def research_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    if not query:
        await _plain(update, "Usage: /research <topic>")
        return
    reply = await route_text(f"research: {query}", update.effective_user.id)
    await _plain(update, reply)


async def deadlines_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = await route_text("show my saved deadlines", update.effective_user.id)
    await _plain(update, reply)


async def saved_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = await route_text("show my saved items", update.effective_user.id)
    await _plain(update, reply)


async def handle_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message.text or "").strip()
    if not text:
        return
    reply = await route_text(text, update.effective_user.id)
    await update.message.reply_text(reply[:4000])