"""Chat and RAG API routes with Bala Buddy persona."""

from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    RetrievedChunk,
    RevisionNotesRequest,
    RevisionNotesResponse,
)
from app.services.guardrails import GREETING_REPLY_EN, GREETING_REPLY_TE, is_greeting
from app.services.llm import generate_grounded_answer, generate_revision_notes
from app.services.progress_service import increment_questions_asked
from app.services.retriever import retrieve

router = APIRouter(prefix="/v1/chat", tags=["Chat & RAG"])


@router.post("", response_model=ChatResponse)
def chat_with_bala_buddy(request: ChatRequest):
    """
    Chat with Bala Buddy (bilingual AI tutor powered by RAG).
    
    1. Retrieves top-k matching chunks from Qdrant vector index.
    2. Enforces syllabus-grounded generation, child-friendly style, and safety guardrails.
    3. Returns kind decline and related syllabus topics if query is out of syllabus.
    4. Automatically increments 'Questions Asked' in student progress.
    """
    if is_greeting(request.query):
        if request.learner_id:
            increment_questions_asked(request.learner_id)
        return ChatResponse(
            query=request.query,
            answer=GREETING_REPLY_TE if request.language == "te" else GREETING_REPLY_EN,
            language=request.language,
            status="answered",
            citations=[],
            retrieved_chunks=[],
            related_topics=[],
        )

    # 1. Retrieve relevant textbook passages from Qdrant
    retrieved_raw = []
    try:
        retrieved_raw = retrieve(
            query=request.query,
            class_name=request.class_name,
            subject=request.subject,
            top_k=5,
        )
        # If no chunks found with specific class filter, broaden retrieval to all classes
        if not retrieved_raw and request.class_name:
            retrieved_raw = retrieve(
                query=request.query,
                class_name=None,
                subject=request.subject,
                top_k=5,
            )
    except Exception as e:  # noqa: BLE001
        print(f"[Retrieval Error] {e}")

    # 2. Generate grounded answer
    answer, status, citations, related_topics = generate_grounded_answer(
        query=request.query,
        retrieved_chunks=retrieved_raw,
        language=request.language,
        subject_hint=request.subject,
        class_name=request.class_name,
    )

    # 3. Log question in student progress
    if request.learner_id:
        increment_questions_asked(request.learner_id)

    # Format chunks for response
    retrieved_models = [
        RetrievedChunk(
            chunk_id=c["chunk_id"],
            subject=c.get("subject", ""),
            chapter=c.get("chapter", ""),
            source_page=c.get("source_page", 1),
            score=round(c.get("score", 0.0), 3),
            text_preview=c.get("text", "")[:120],
        )
        for c in retrieved_raw
    ]

    return ChatResponse(
        query=request.query,
        answer=answer,
        language=request.language,
        status=status,
        citations=citations,
        retrieved_chunks=retrieved_models,
        related_topics=related_topics,
    )


@router.post("/revision-notes", response_model=RevisionNotesResponse)
def get_revision_notes(request: RevisionNotesRequest):
    """Generate structured revision notes for a chapter or topic."""
    # Retrieve relevant chapter chunks
    retrieved_raw = []
    try:
        retrieved_raw = retrieve(
            query=f"{request.subject} {request.chapter}",
            class_name=request.class_name,
            subject=request.subject,
            top_k=3,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[Revision Retrieval Error] {e}")

    notes_data = generate_revision_notes(
        chapter=request.chapter,
        subject=request.subject,
        language=request.language,
        retrieved_chunks=retrieved_raw,
    )
    return RevisionNotesResponse(**notes_data)
