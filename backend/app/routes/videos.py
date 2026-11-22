"""Video metadata and streaming API routes.

Adheres to:
- [PS: 7. Video Section]
- [PS: Online Mode "Video Streaming"]
- [Arch: Data model, Videos]
- [Arch: Data flow (c)]
"""

from fastapi import APIRouter, HTTPException, Query

from app.schemas.videos import TopicVideosResponse, VideoItem
from app.services.video_service import get_video_by_id, list_videos_for_topic

router = APIRouter(prefix="/v1", tags=["Videos"])


@router.get("/topics/{topic_id}/videos", response_model=TopicVideosResponse)
def get_topic_videos(
    topic_id: str,
    language: str | None = Query(default=None, description="Optional language filter: 'te' or 'en'"),
):
    """
    Get educational videos for a specific topic.
    Returns both Telugu and English videos where available [PS: 7. Video Section].
    """
    videos = list_videos_for_topic(topic_id, language=language)
    if not videos:
        # If no specific video found, check if it's a known topic
        raise HTTPException(status_code=404, detail=f"No videos found for topic '{topic_id}'")

    return TopicVideosResponse(
        topic_id=topic_id,
        total_count=len(videos),
        videos=videos,
    )


@router.get("/videos/{video_id}", response_model=VideoItem)
def get_video_details(video_id: str):
    """
    Get metadata, quality tiers, and stream endpoint for a specific video.
    Note: Media itself streams online only over HTTPS/HLS; no media binary is stored.
    """
    video = get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' not found")
    return video
