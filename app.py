"""Entry point: runs the Telegram bot with long polling (Heroku worker)."""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import settings
from bot.handlers import (
    start, help_cmd, status_cmd, search_cmd, universities_cmd,
    programmes_cmd, scholarships_cmd, research_cmd, deadlines_cmd,
    saved_cmd, handle_free_text,
)

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("scholarship_assistant")


def main() -> None:
    log.info("Starting bot...")
    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("search", search_cmd))
    app.add_handler(CommandHandler("universities", universities_cmd))
    app.add_handler(CommandHandler("programmes", programmes_cmd))
    app.add_handler(CommandHandler("scholarship", scholarships_cmd))
    app.add_handler(CommandHandler("research", research_cmd))
    app.add_handler(CommandHandler("deadlines", deadlines_cmd))
    app.add_handler(CommandHandler("saved", saved_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_text))

    log.info("Bot is polling. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()