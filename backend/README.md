# Backend (FastAPI)

Setup (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements-dev.txt

Run tests: `python -m pytest`
Lint: `python -m ruff check .`
Run server: `uvicorn app.main:app --reload`

Planned route prefixes (provisional, from docs/architecture.md): /v1/classes, /v1/search, /v1/chat, /v1/progress, /v1/sync, /v1/analytics.
