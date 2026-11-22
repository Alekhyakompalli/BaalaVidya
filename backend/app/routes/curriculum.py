"""Curriculum API routes."""


from fastapi import APIRouter, HTTPException, Query

from app.schemas.curriculum import (
    ChapterItem,
    ChapterPackageResponse,
    ClassItem,
    LatestUpdateItem,
    SubjectItem,
)
from app.services.curriculum_service import (
    get_chapter_package,
    get_latest_updates,
    get_topic_pdf_passage,
    list_chapters_for_subject,
    list_classes,
    list_subjects_for_class,
)

router = APIRouter(prefix="/v1", tags=["Curriculum"])


@router.get("/classes", response_model=list[ClassItem])
def get_classes():
    """List all available classes (Class 1 to 10)."""
    return list_classes()


@router.get("/classes/{class_id}/subjects", response_model=list[SubjectItem])
def get_subjects(
    class_id: str,
    medium: str | None = Query(default=None, description="Optional medium filter (EM for English Medium, TM for Telugu Medium)"),
):
    """List subjects for a specified class."""
    return list_subjects_for_class(class_id, medium=medium)


@router.get("/classes/{class_id}/subjects/{subject_id}/chapters", response_model=list[ChapterItem])
def get_chapters(class_id: str, subject_id: str):
    """List chapters and topics for a subject."""
    chapters = list_chapters_for_subject(class_id, subject_id)
    if not chapters and str(class_id) == "10":
        raise HTTPException(status_code=404, detail="Subject not found")
    return chapters


@router.get("/curriculum/latest-updates", response_model=list[LatestUpdateItem])
def get_updates(class_id: str | None = Query(default=None, description="Optional class filter")):
    """Get latest curriculum announcements, challenges, and exam updates."""
    return get_latest_updates(class_id)


@router.get("/curriculum/packages/{subject_id}/{chapter_id}", response_model=ChapterPackageResponse)
def get_package(subject_id: str, chapter_id: str):
    """Download versioned offline package for a chapter."""
    pkg = get_chapter_package(subject_id, chapter_id)
    if not pkg:
        raise HTTPException(status_code=404, detail="Chapter package not found")
    return pkg


@router.get("/curriculum/topic-pdf-passage")
def get_topic_passage(
    topic: str = Query(..., description="Topic name to look up in SCERT textbook PDF"),
    subject: str | None = Query(default=None, description="Optional subject filter"),
    medium: str = Query(default="EM", description="EM or TM"),
    chapter: str | None = Query(default=None, description="Optional chapter name"),
    class_id: str = Query(default="10", description="Class level: 6, 7, 8, 9, 10"),
):
    """Retrieve detailed explanation and textbook excerpt directly from SCERT PDF."""
    return get_topic_pdf_passage(topic=topic, subject=subject, medium=medium, chapter=chapter, class_id=class_id)

