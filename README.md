# Scholarship & Research Assistant (Telegram Bot)

A Python Telegram bot that searches universities, programmes, scholarships,
and research using Brave Search + Supabase + an OpenAI-compatible AI provider.

## Quick start (Windows 11, VS Code)

```powershell
# 1. Virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 3. Create your .env from the template
Copy-Item .env.example .env
# Then open .env in VS Code and fill in the real values.

# 4. Sanity check
python scripts/check_env.py

# 5. Run the bot
python app.py

Copy-Item .env.example .env
notepad .env





$env_content = @'
# ---------- Telegram ----------
TELEGRAM_BOT_TOKEN=
ADMIN_TELEGRAM_IDS=

# ---------- Supabase ----------
SUPABASE_URL=
SUPABASE_SECRET_KEY=
SUPABASE_PUBLISHABLE_KEY=

# ---------- Brave Search ----------
BRAVE_SEARCH_API_KEY=

# ---------- AI Provider ----------
AI_PROVIDER=openai
AI_API_KEY=
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini

# ---------- App ----------
TIMEZONE=UTC
LOG_LEVEL=INFO