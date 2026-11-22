"""Retriever service querying the Phase 1 Qdrant pilot index."""

from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.config import settings

_client: QdrantClient | None = None
_model: Any = None


def get_qdrant_client() -> QdrantClient:
    """Return singleton QdrantClient connected to local pilot store."""
    global _client
    if _client is None:
        p = Path(settings.QDRANT_PATH)
        if not p.exists():
            raise FileNotFoundError(f"Qdrant store not found at {p}. Run Phase 1 ingestion first.")
        _client = QdrantClient(path=str(p))
    return _client


def get_embedding_model():
    """Return singleton SentenceTransformer model for query encoding."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(settings.EMBEDDING_MODEL, local_files_only=True)
    return _model


def retrieve(
    query: str,
    class_name: str | None = "10",
    subject: str | None = None,
    top_k: int = 5,
    score_threshold: float | None = None,
) -> list[dict[str, Any]]:
    """Retrieve top matching chunks from Qdrant with optional class and subject filtering."""
    if score_threshold is None:
        score_threshold = settings.SCORE_THRESHOLD

    client = get_qdrant_client()
    model = get_embedding_model()

    # Prepend query: prefix required by multilingual-e5-base
    query_text = f"query: {query.strip()}"
    qvec = model.encode(query_text, normalize_embeddings=True).tolist()

    # Build Qdrant filter
    conditions = []
    if class_name:
        conditions.append(FieldCondition(key="class", match=MatchValue(value=str(class_name))))
    if subject:
        conditions.append(FieldCondition(key="subject", match=MatchValue(value=str(subject))))

    q_filter = Filter(must=conditions) if conditions else None

    # Query Qdrant
    search_res = client.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=qvec,
        query_filter=q_filter,
        limit=top_k,
        with_payload=True,
    ).points

    hits = []
    for hit in search_res:
        score = float(hit.score)
        if score >= score_threshold:
            payload = hit.payload or {}
            hits.append({
                "chunk_id": payload.get("chunk_id", str(hit.id)),
                "subject": payload.get("subject", ""),
                "chapter": payload.get("chapter", ""),
                "source_page": payload.get("source_page", 1),
                "language": payload.get("language", "en"),
                "score": score,
                "text": payload.get("text_preview", "") or payload.get("text", ""),
                "full_text": payload.get("text", "") or payload.get("text_preview", ""),
            })

    return hits
