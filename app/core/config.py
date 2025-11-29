"""Application configuration helpers."""
from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = "IsCoolGPT API"
    port: int = 8000
    api_key: str | None = None
    # Default model compatible with google-generativeai v1 API.
    gemini_model: str = "gemini-2.5-flash"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"


def load_settings() -> Settings:
    """
    Load application settings from environment variables with safe fallbacks.
    """
    env_port = os.getenv("PORT", "8000")
    try:
        port_value = int(env_port)
    except ValueError:
        port_value = 8000

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")

    return Settings(
        port=port_value,
        api_key=api_key,
        gemini_model=os.getenv("GEMINI_MODEL", Settings.gemini_model),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", Settings.openai_model),
    )
