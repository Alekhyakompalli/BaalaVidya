"""Search API routes."""


from fastapi import APIRouter, Query

from app.schemas.search import SearchResponse
from app.services.search_service import search_syllabus_and_chunks

router = APIRouter(prefix="/v1", tags=["Search"])


@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., description="Search query string"),
    class_name: str | None = Query(default=None, description="Optional class level filter (6, 7, 8, 9, 10 or None for all classes)"),
    subject: str | None = Query(default=None, description="Optional subject filter"),
    limit: int = Query(default=10, ge=1, le=50, description="Max results to return"),
):
    """Search across syllabus topics, chapters, and indexed textbook passages."""
    return search_syllabus_and_chunks(
        query=q,
        class_name=class_name,
        subject=subject,
        limit=limit,
    )
