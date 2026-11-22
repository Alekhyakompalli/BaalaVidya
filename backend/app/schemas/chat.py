"""Chat and RAG Pydantic schemas."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., description="Student's question or greeting")
    language: str = Field(default="en", description="Selected language: 'en' (English) or 'te' (Telugu)")
    class_name: str | None = Field(default="10", description="Student's class (default '10')")
    subject: str | None = Field(default=None, description="Optional subject filter (e.g. 'Biology', 'Mathematics')")
    learner_id: str | None = Field(default="learner_guest", description="Learner identifier for tracking progress")


class RetrievedChunk(BaseModel):
    chunk_id: str
    subject: str
    chapter: str
    source_page: int
    score: float
    text_preview: str


class ChatResponse(BaseModel):
    query: str
    answer: str
    language: str
    status: str = Field(description="'answered' (grounded), 'declined' (out-of-syllabus), or 'refused' (safety guardrail)")
    citations: list[str] = Field(default_factory=list, description="Chunk IDs cited by the answer")
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list, description="Chunks retrieved from Qdrant index")
    suggested_next_steps: list[str] = Field(
        default_factory=lambda: ["Play Game", "Practice Workbook", "Watch Video", "Ask Doubts"],
        description="Bala Buddy interactive next steps"
    )
    related_topics: list[str] = Field(default_factory=list, description="Related syllabus topics offered during kind declines")


class RevisionNotesRequest(BaseModel):
    chapter: str = Field(..., description="Chapter name (e.g. 'Lesson 1', 'Chapter 1')")
    subject: str = Field(..., description="Subject name (e.g. 'Biology', 'Mathematics')")
    class_name: str = Field(default="10", description="Class (default '10')")
    language: str = Field(default="en", description="Language: 'en' or 'te'")


class RevisionNotesResponse(BaseModel):
    chapter: str
    subject: str
    language: str
    title: str
    key_concepts: list[str]
    summary: str
    important_questions: list[str]
    citations: list[str]
