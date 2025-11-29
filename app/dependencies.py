from fastapi import Request

from app.core.config import Settings


def get_settings(request: Request) -> Settings:
    """Access application settings stored on the app state."""
    return request.app.state.settings
