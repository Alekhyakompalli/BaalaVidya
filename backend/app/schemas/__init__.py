"""App schemas module."""

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    RetrievedChunk,
    RevisionNotesRequest,
    RevisionNotesResponse,
)
from app.schemas.curriculum import (
    ChapterItem,
    ClassItem,
    LatestUpdateItem,
    SubjectItem,
    TopicItem,
)
from app.schemas.progress import (
    ActivityLogRequest,
    ProgressResponse,
)
from app.schemas.search import (
    SearchResponse,
    SearchResultItem,
)

__all__ = [
    "ActivityLogRequest",
    "ChapterItem",
    "ChatRequest",
    "ChatResponse",
    "ClassItem",
    "LatestUpdateItem",
    "ProgressResponse",
    "RetrievedChunk",
    "RevisionNotesRequest",
    "RevisionNotesResponse",
    "SearchResponse",
    "SearchResultItem",
    "SubjectItem",
    "TopicItem",
]
