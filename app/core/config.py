"""Application configuration helpers."""
from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = "IsCoolGPT API"
    port: int = 8000
    api_key: str | None = None
    # Default to a model supported by the installed google-generativeai version.
    gemini_model: str = "gemini-1.5-flash"


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
    )
