import os
from dataclasses import dataclass
from typing import Optional

from fastapi import FastAPI

from app.api.routes import router


@dataclass
class Settings:
    port: int = 8000
    api_key: Optional[str] = None


def load_settings() -> Settings:
    """
    Load application settings from environment variables.
    Falls back to sensible defaults when variables are missing or invalid.
    """
    env_port = os.getenv("PORT", "8000")
    try:
        port_value = int(env_port)
    except ValueError:
        port_value = 8000

    return Settings(port=port_value, api_key=os.getenv("API_KEY"))


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="IsCoolGPT API")
    app.state.settings = load_settings()
    app.include_router(router)
    return app


app = create_app()

