"""Central configuration loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    telegram_bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")
    admin_telegram_ids: str = Field("", alias="ADMIN_TELEGRAM_IDS")

    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_secret_key: str = Field(..., alias="SUPABASE_SECRET_KEY")
    supabase_publishable_key: str = Field("", alias="SUPABASE_PUBLISHABLE_KEY")

    brave_search_api_key: str = Field("", alias="BRAVE_SEARCH_API_KEY")

    ai_provider: str = Field("openai", alias="AI_PROVIDER")
    ai_api_key: str = Field("", alias="AI_API_KEY")
    ai_base_url: str = Field("https://api.openai.com/v1", alias="AI_BASE_URL")
    ai_model: str = Field("gpt-4o-mini", alias="AI_MODEL")

    timezone: str = Field("UTC", alias="TIMEZONE")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    @property
    def admin_ids(self) -> list[int]:
        return [int(x.strip()) for x in self.admin_telegram_ids.split(",") if x.strip().isdigit()]


settings = Settings()