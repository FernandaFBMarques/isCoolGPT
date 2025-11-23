from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_main() -> str:
    """Simple HTML landing page for the IsCoolGPT API."""
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>IsCoolGPT</title>
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #e5e7eb;
          }
          .card {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 16px;
            padding: 32px 40px;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.6);
            max-width: 520px;
            width: 100%;
          }
          h1 {
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 28px;
          }
          p {
            margin-top: 4px;
            margin-bottom: 16px;
            line-height: 1.5;
          }
          .links {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 16px;
          }
          a {
            text-decoration: none;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid #38bdf8;
            color: #e5e7eb;
            font-size: 14px;
          }
          a.primary {
            background: #0ea5e9;
            border-color: #0ea5e9;
            color: #0f172a;
            font-weight: 600;
          }
          small {
            display: block;
            margin-top: 20px;
            color: #9ca3af;
            font-size: 12px;
          }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>IsCoolGPT API</h1>
          <p>
            This FastAPI application is running on AWS ECS Fargate.
            Use the links below to explore the API and check its health.
          </p>
          <div class="links">
            <a href="/docs" class="primary">Open API docs (/docs)</a>
            <a href="/ping">Health check (/ping)</a>
          </div>
          <small>Cloud Computing final project – IsCoolGPT.</small>
        </div>
      </body>
    </html>
    """


@router.get("/ping")
async def get_ping() -> dict[str, str]:
    """Healthcheck endpoint used to verify the service is up."""
    return {"message": "pong"}

