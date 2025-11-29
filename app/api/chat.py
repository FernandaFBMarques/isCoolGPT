from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.core.config import Settings
from app.dependencies import get_settings
from app.services.gemini import generate_reply


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="User prompt")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Model-generated reply")


router = APIRouter(tags=["chat"])


@router.get("/chat", response_model=ChatResponse)
def get_chat(
    message: str = Query(
        "ping",
        min_length=1,
        max_length=4000,
        description="User prompt",
    ),
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    """Allow chatting via GET (useful for quick tests or ALB health checks)."""
    reply_text = generate_reply(settings, message)
    return ChatResponse(reply=reply_text)


@router.post("/chat", response_model=ChatResponse)
def post_chat(request: ChatRequest, settings: Settings = Depends(get_settings)) -> ChatResponse:
    """Send a prompt to the Gemini API and return the generated reply."""
    reply_text = generate_reply(settings, request.message)
    return ChatResponse(reply=reply_text)
