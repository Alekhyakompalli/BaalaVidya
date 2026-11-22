"""Curriculum Pydantic schemas."""


from pydantic import BaseModel


class TopicItem(BaseModel):
    topic_id: str
    chapter_id: str
    order: int
    title: str
    summary: str | None = None


class ChapterItem(BaseModel):
    chapter_id: str
    subject_id: str
    order: int
    title: str
    topics: list[TopicItem] = []


class SubjectItem(BaseModel):
    subject_id: str
    class_id: str
    name: str
    medium: str  # EM, TM, BIL
    icon: str | None = None
    chapters_count: int = 0


class ClassItem(BaseModel):
    class_id: str
    number: int
    name: str
    subjects_count: int = 0


class LatestUpdateItem(BaseModel):
    update_id: str
    title: str
    description: str
    date: str
    category: str
    class_id: str | None = "10"
    subject_id: str | None = None


class VectorSliceItem(BaseModel):
    chunk_id: str
    text: str
    subject: str
    chapter: str
    source_page: int
    language: str


class VideoMetadataItem(BaseModel):
    video_id: str
    topic_id: str | None = None
    language_code: str = "te"
    title: str
    telugu_title: str
    duration_minutes: int
    duration_seconds: int = 0
    stream_url: str | None = None
    provider: str = "T-SAT Vidya / SCERT Telangana"
    online_streaming_only: bool = True


class WorkbookActivityItem(BaseModel):
    activity_id: str
    topic_id: str
    question: str
    telugu_question: str
    options: list[str]
    telugu_options: list[str]
    correct_index: int
    explanation: str
    telugu_explanation: str


class EducationalGameItem(BaseModel):
    game_id: str
    title: str
    telugu_title: str
    game_type: str
    items: list[dict]


class ChapterPackageResponse(BaseModel):
    package_version: str = "1.0.0"
    subject_id: str
    chapter_id: str
    class_id: str = "10"
    title: str
    telugu_title: str
    topics: list[dict]
    workbook_activities: list[WorkbookActivityItem]
    educational_games: list[EducationalGameItem]
    cached_video_metadata: list[VideoMetadataItem]
    vector_db_slice: list[VectorSliceItem]
    size_bytes: int
    checksum: str
