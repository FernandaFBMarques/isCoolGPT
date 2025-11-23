# IsCoolGPT — Intelligent Study Assistant for Cloud Computing

IsCoolGPT is a lightweight FastAPI backend that provides an intelligent study assistant for Cloud Computing topics. This repository contains the application code and a Docker setup for easy local development and containerized deployment. This project was developed as the final project for a Cloud Computing course.

## How to run locally

1. Create and activate a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Export your Gemini API key (supports either `GEMINI_API_KEY` or `API_KEY`):

```bash
export GEMINI_API_KEY="your-gemini-key"
# or: export API_KEY="your-gemini-key"
```

3. Start the app with Uvicorn (run from the project root):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

4. Open the chat UI and API docs:
  - Swagger UI: http://127.0.0.1:8000/docs
  - ReDoc: http://127.0.0.1:8000/redoc
  - Chat UI: http://127.0.0.1:8000/main (posts to `/chat`)

Notes:
- Use `--reload` for development to enable auto-reload on code changes.
- If your FastAPI `app` is at a different import path, point `uvicorn` at the module that exposes the `app` instance.

## How to run with Docker

The Dockerfile used in this project exposes `PORT=8000`. From the repository root (or the directory containing the `Dockerfile`), run:

```bash
docker build -t iscoolgpt:latest .
docker run --rm -p 8000:8000 iscoolgpt:latest
```

Visit `http://localhost:8000/docs` to access the API docs when the container is running.

If you prefer a different host port, change the left side of `-p`, for example `-p 8080:8000`.

## Technologies used

- **FastAPI** — API framework
- **Uvicorn** — ASGI server for FastAPI
- **Python 3.x** — application language/runtime
- **Docker** — containerization
- **Git / GitHub** — source control
- **GitHub Actions** — CI/CD (scaffold added; full pipelines to be extended)
- **AWS ECR / ECS** — container registry and hosting (CI/CD and deployment will be added later)

---

If you want, I can:
- Create the Pull Request for these changes (I have already pushed branch `add-readme-ci`).
- Extend the CI workflow to push to ECR and deploy to ECS (needs credentials/secrets).
- Add a small smoke test to validate the API root endpoint.
# isCoolGPT
IsCoolGPT – Intelligent Study Assistant for Cloud Computing
