"""Configuration settings for BAALAVIDYA FastAPI backend."""

import os
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

QDRANT_DEFAULT_PATH = PROJECT_ROOT / "ingestion" / "data" / "qdrant_local"
CHUNKS_DEFAULT_PATH = PROJECT_ROOT / "ingestion" / "data" / "chunks" / "class10_pilot.jsonl"

class Settings:
    PROJECT_NAME: str = "BAALAVIDYA API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    # Vector store
    QDRANT_PATH: str = os.getenv("QDRANT_PATH", str(QDRANT_DEFAULT_PATH))
    CHUNKS_PATH: str = os.getenv("CHUNKS_PATH", str(CHUNKS_DEFAULT_PATH))
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "pilot_chunks")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
    SCORE_THRESHOLD: float = float(os.getenv("SCORE_THRESHOLD", "0.82"))
    TOP_K: int = int(os.getenv("TOP_K", "5"))

    # LLM Settings (Phase 0 / R3 choice: Azure OpenAI / OpenAI compatible)
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Offline / HuggingFace settings
    HF_HUB_OFFLINE: str = os.getenv("HF_HUB_OFFLINE", "1")
    TRANSFORMERS_OFFLINE: str = os.getenv("TRANSFORMERS_OFFLINE", "1")

settings = Settings()

# Ensure offline mode variables are set in process environment
os.environ["HF_HUB_OFFLINE"] = settings.HF_HUB_OFFLINE
os.environ["TRANSFORMERS_OFFLINE"] = settings.TRANSFORMERS_OFFLINE
