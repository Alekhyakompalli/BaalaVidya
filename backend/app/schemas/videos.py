"""Pydantic schemas for the Videos entity and Metadata API.

Adheres to:
- [PS: 7. Video Section]
- [Arch: Data model, Videos (`video_id`, `topic_id`, `language_code`, `title`, `url`, `duration`)]
- [Arch: Data flow (c) Student opens a topic and watches a video]
"""

from pydantic import BaseModel, Field


class VideoQualityLevel(BaseModel):
    label: str = Field(..., description="Display label (e.g., 360p Data Saver, 480p Standard, 720p HD)")
    resolution: str = Field(..., description="Resolution string: 360p, 480p, 720p")
    stream_url: str = Field(..., description="HLS / HTTPS streaming URL for this quality level")


class VideoItem(BaseModel):
    video_id: str = Field(..., description="Unique video identifier")
    topic_id: str = Field(..., description="Associated topic identifier")
    language_code: str = Field(..., description="Language code: 'te' (Telugu) or 'en' (English)")
    title: str = Field(..., description="English title")
    telugu_title: str = Field(..., description="Telugu title")
    description: str = Field(..., description="English lesson description")
    telugu_description: str = Field(..., description="Telugu lesson description")
    duration_seconds: int = Field(..., description="Duration in seconds")
    duration_minutes: int = Field(..., description="Duration in whole minutes")
    url: str = Field(..., description="Primary HLS / HTTPS video stream URL")
    provider: str = Field(default="T-SAT Vidya / SCERT Telangana", description="Content publisher or broadcast provider")
    quality_levels: list[VideoQualityLevel] = Field(default_factory=list, description="Adaptive bitrate options")
    online_streaming_only: bool = Field(default=True, description="Strict flag enforcing online streaming only")
    thumbnail_icon: str = Field(default="🎬", description="Friendly UI thumbnail icon or badge")


class TopicVideosResponse(BaseModel):
    topic_id: str
    total_count: int
    videos: list[VideoItem]
