from fastapi import APIRouter, Depends, Query

from app.api.chat import ChatRequest, ChatResponse
from app.core.config import Settings
from app.dependencies import get_settings
from app.services.openai_client import generate_reply_openai

router = APIRouter(tags=["chatgpt"])


@router.get("/chatgpt", response_model=ChatResponse)
def get_chatgpt(
    message: str = Query(
        "ping",
        min_length=1,
        max_length=4000,
        description="User prompt",
    ),
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    """Allow chatting via GET using OpenAI (useful for quick tests)."""
    reply_text = generate_reply_openai(settings, message)
    return ChatResponse(reply=reply_text)


@router.post("/chatgpt", response_model=ChatResponse)
def post_chatgpt(request: ChatRequest, settings: Settings = Depends(get_settings)) -> ChatResponse:
    """Send a prompt to OpenAI Chat Completions and return the generated reply."""
    reply_text = generate_reply_openai(settings, request.message)
    return ChatResponse(reply=reply_text)
