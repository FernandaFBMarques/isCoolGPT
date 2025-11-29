from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/web/templates")

router = APIRouter(tags=["web"])


@router.get("/", response_class=HTMLResponse)
@router.get("/main", response_class=HTMLResponse)
async def render_chat(request: Request) -> HTMLResponse:
    """Serve the chat UI (kept alongside the API for simplicity)."""
    return templates.TemplateResponse("chat.html", {"request": request})
