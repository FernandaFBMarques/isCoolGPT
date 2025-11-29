"""Helpers to configure and call the Gemini API."""
import logging
from functools import lru_cache
from typing import Any

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import Settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _init_model(api_key: str, model_name: str) -> genai.GenerativeModel:
    """Initialize and cache the Gemini model for reuse across requests."""
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_name)
    except Exception as exc:  # pragma: no cover - defensive path
        logger.exception("Gemini init failed (model=%s)", model_name)
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize Gemini model. Check API key and model name.",
        ) from exc


def generate_reply(settings: Settings, message: str) -> str:
    """Send a prompt to Gemini and return the generated text."""
    if not settings.api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured.")

    model = _init_model(settings.api_key, settings.gemini_model)

    try:
        result: Any = model.generate_content(message)
        reply_text = (getattr(result, "text", "") or "").strip()
    except Exception as exc:  # pragma: no cover - defensive path
        logger.exception("Gemini request failed for message length=%s", len(message))
        raise HTTPException(status_code=502, detail="Gemini API request failed.") from exc

    if not reply_text:
        logger.error("Gemini returned empty text for message length=%s", len(message))
        raise HTTPException(status_code=502, detail="Gemini API returned an empty response.")

    return reply_text
