"""Pydantic schemas for the Sync service.

Adheres to [Arch: Sync rules 1, 2, 3, 4, 7; Plan: Phase 6].
"""

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.progress import ProgressResponse


class SyncEventItem(BaseModel):
    event_id: str = Field(..., description="Unique event identifier (UUID or timestamped)")
    client_id: str = Field(..., description="Originating client device identifier")
    learner_id: str = Field(..., description="Target learner identifier")
    event_type: str = Field(..., description="topic_read, workbook_completed, game_played, question_asked, streak_update")
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(..., description="ISO 8601 event timestamp")


class SyncBatchRequest(BaseModel):
    learner_id: str = Field(..., description="Student learner ID")
    device_id: str = Field(..., description="Device ID sending the batch")
    events: list[SyncEventItem] = Field(default_factory=list, description="Ordered progress events batch")


class SyncBatchResponse(BaseModel):
    status: str = "success"
    learner_id: str
    processed_count: int
    duplicate_count: int
    progress: ProgressResponse
