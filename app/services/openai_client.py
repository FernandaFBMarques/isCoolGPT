"""Helpers to configure and call the OpenAI Chat Completions API."""
import logging
from functools import lru_cache

from fastapi import HTTPException
from openai import OpenAI

from app.core.config import Settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client(api_key: str) -> OpenAI:
    """Create and cache the OpenAI client."""
    return OpenAI(api_key=api_key)


def generate_reply_openai(settings: Settings, message: str) -> str:
    """
    Send a prompt to OpenAI and return the generated text.
    Uses the chat completions endpoint with a single user message.
    """
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured.")

    client = _client(settings.openai_api_key)
    try:
        completion = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "user", "content": message}],
        )
        reply_text = completion.choices[0].message.content.strip()
    except Exception as exc:  # pragma: no cover - defensive path
        logger.exception("OpenAI request failed for message length=%s", len(message))
        raise HTTPException(status_code=502, detail="OpenAI API request failed.") from exc

    if not reply_text:
        logger.error("OpenAI returned empty text for message length=%s", len(message))
        raise HTTPException(status_code=502, detail="OpenAI API returned an empty response.")

    return reply_text
