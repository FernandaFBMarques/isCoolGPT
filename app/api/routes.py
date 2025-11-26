import os
from typing import Optional

import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

router = APIRouter()


def _configure_gemini() -> Optional[genai.GenerativeModel]:
    """
    Configure and return a Gemini model instance.
    Supports either GEMINI_API_KEY or API_KEY environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


_gemini_model = _configure_gemini()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="User prompt")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Model-generated reply")


@router.get("/main", response_class=HTMLResponse)
async def get_main() -> str:
    """Serve a simple chat backed by the Gemini API."""
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>IsCoolGPT – Gemini Chat</title>
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: grid;
            place-items: center;
            min-height: 100vh;
            margin: 0;
            background: radial-gradient(circle at 20% 20%, #0ea5e920 0, #0f172a 25%, #0b1224 55%), #0b1224;
            color: #e2e8f0;
          }
          .shell {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 18px;
            padding: 28px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
            width: min(960px, 100%);
            margin: 24px;
            border: 1px solid rgba(56, 189, 248, 0.25);
          }
          h1 {
            margin: 0 0 6px;
            font-size: 26px;
            letter-spacing: -0.02em;
          }
          p {
            margin: 4px 0 18px;
            line-height: 1.5;
            color: #cbd5e1;
          }
          .chat-window {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            padding: 16px;
            height: 340px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 16px;
          }
          .bubble {
            max-width: 80%;
            padding: 12px 14px;
            border-radius: 12px;
            font-size: 15px;
            line-height: 1.5;
            word-break: break-word;
            white-space: pre-wrap;
          }
          .user {
            align-self: flex-end;
            background: #0ea5e9;
            color: #0b1224;
          }
          .assistant {
            align-self: flex-start;
            background: rgba(226, 232, 240, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.35);
          }
          form {
            display: flex;
            gap: 12px;
            align-items: center;
          }
          textarea {
            flex: 1;
            resize: vertical;
            min-height: 72px;
            max-height: 180px;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.4);
            background: rgba(15, 23, 42, 0.8);
            color: #e2e8f0;
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
          }
          textarea:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
          }
          button {
            background: linear-gradient(135deg, #22d3ee, #0ea5e9);
            color: #0b1224;
            border: none;
            border-radius: 12px;
            padding: 12px 18px;
            font-weight: 700;
            cursor: pointer;
            min-width: 120px;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
          }
          button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 20px rgba(14, 165, 233, 0.35);
          }
          button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
          }
          .links {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
          }
          .links a {
            text-decoration: none;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid #38bdf8;
            color: #e2e8f0;
            font-size: 14px;
          }
          .hint {
            color: #94a3b8;
            font-size: 13px;
            margin-top: 6px;
          }
          .error {
            color: #fca5a5;
            font-size: 14px;
            margin-top: 8px;
          }
          @media (max-width: 720px) {
            .shell { padding: 20px; }
            .chat-window { height: 260px; }
            button { min-width: 96px; }
          }
        </style>
      </head>
      <body>
        <div class="shell">
          <h1>IsCoolGPT · Gemini Chat</h1>
          <p>Ask anything about cloud computing or your coursework. Responses are powered by Google's Gemini API.</p>

          <div id="chat" class="chat-window"></div>

          <form id="chat-form">
            <textarea id="message" name="message" placeholder="Type a question..." required></textarea>
            <button type="submit" id="send-btn">Send</button>
          </form>
          <div class="hint">API endpoints: /chat (POST), /ping (GET), /docs.</div>
          <div id="error" class="error" style="display:none;"></div>

          <div class="links">
            <a href="/docs">Swagger docs</a>
            <a href="/ping">Health check</a>
          </div>
        </div>

        <script>
          const chat = document.getElementById("chat");
          const form = document.getElementById("chat-form");
          const textarea = document.getElementById("message");
          const errorBox = document.getElementById("error");
          const sendBtn = document.getElementById("send-btn");

          const pushMessage = (role, text) => {
            const bubble = document.createElement("div");
            bubble.className = `bubble ${role}`;
            bubble.textContent = text;
            chat.appendChild(bubble);
            chat.scrollTop = chat.scrollHeight;
          };

          form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const message = textarea.value.trim();
            if (!message) return;

            errorBox.style.display = "none";
            pushMessage("user", message);
            textarea.value = "";
            textarea.focus();
            sendBtn.disabled = true;
            sendBtn.textContent = "Thinking...";

            try {
              const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
              });

              if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                const detail = data.detail || "Unable to reach the model right now.";
                throw new Error(detail);
              }

              const data = await response.json();
              pushMessage("assistant", data.reply || "No response from the model.");
            } catch (err) {
              errorBox.textContent = err.message || "Something went wrong.";
              errorBox.style.display = "block";
            } finally {
              sendBtn.disabled = false;
              sendBtn.textContent = "Send";
            }
          });
        </script>
      </body>
    </html>
    """


@router.get("/ping")
async def get_ping() -> dict[str, str]:
    """Healthcheck endpoint used to verify the service is up."""
    return {"message": "pong"}


@router.post("/chat", response_model=ChatResponse)
def post_chat(request: ChatRequest) -> ChatResponse:
    """Send a prompt to the Gemini API and return the generated reply."""
    if _gemini_model is None:
        raise HTTPException(status_code=500, detail="Gemini API key not configured.")

    try:
        result = _gemini_model.generate_content(request.message)
        reply_text = (result.text or "").strip()
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(status_code=502, detail="Gemini API request failed.") from exc

    if not reply_text:
        raise HTTPException(status_code=502, detail="Gemini API returned an empty response.")

    return ChatResponse(reply=reply_text)
