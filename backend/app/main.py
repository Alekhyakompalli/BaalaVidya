"""BAALAVIDYA FastAPI backend application.

Serves Curriculum, Search, Chat/RAG (Bala Buddy), and Progress services.
"""

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import settings
from app.routes.analytics import router as analytics_router
from app.routes.chat import router as chat_router
from app.routes.curriculum import router as curriculum_router
from app.routes.health import router as health_router
from app.routes.pilot import router as pilot_router
from app.routes.progress import router as progress_router
from app.routes.search import router as search_router
from app.routes.sync import router as sync_router
from app.routes.videos import router as videos_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API services for BAALAVIDYA - Child-Friendly Bilingual Learning Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware for Flutter web and local frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register service routers
app.include_router(health_router)
app.include_router(curriculum_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(progress_router)
app.include_router(sync_router)
app.include_router(videos_router)
app.include_router(analytics_router)
app.include_router(pilot_router)


@app.get("/app", response_class=HTMLResponse, tags=["Web App"])
def web_app():
    """Interactive BAALAVIDYA web client showcasing all features locally."""
    html_file = Path(__file__).parent / "static" / "app.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>BAALAVIDYA Web App</h1><p>Static file not found.</p>")


@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "web_app": "/app",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    # Railway injects PORT; fall back to 8000 for local runs.
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
