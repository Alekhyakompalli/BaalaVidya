"""Tests for Phase 7 Video Section API, Metadata Caching, and Progress Syncing.

Adheres to:
- [PS: 7. Video Section]
- [PS: Online Mode "Video Streaming"]
- [Arch: Data model, Videos]
- [Arch: Data flow (c)]
- Phase 7 Exit Criteria:
  1. No video file is stored offline (streaming only, metadata caching).
  2. Metadata lists correctly in both languages (Telugu and English).
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.progress_service import _LEARNER_DB
from app.services.sync_service import reset_sync_state

client = TestClient(app)


def setup_function():
    """Reset state before each test."""
    reset_sync_state()
    _LEARNER_DB.clear()


def test_get_videos_for_topic_returns_both_languages():
    """Exit Criterion 2: Telugu and English video list per topic, with both shown where available."""
    response = client.get("/v1/topics/bio_ch1_t1/videos")
    assert response.status_code == 200
    data = response.json()

    assert data["topic_id"] == "bio_ch1_t1"
    assert data["total_count"] >= 2

    languages = [v["language_code"] for v in data["videos"]]
    assert "te" in languages, "Expected Telugu explanation video"
    assert "en" in languages, "Expected English explanation video"

    # Verify video properties adhere to Videos data model
    for v in data["videos"]:
        assert v["video_id"].startswith("vid_")
        assert len(v["title"]) > 5
        assert len(v["telugu_title"]) > 5
        assert v["duration_minutes"] > 0
        assert v["duration_seconds"] > 0
        assert v["url"].startswith("https://")
        assert v["online_streaming_only"] is True, "Exit Criterion 1: Must be online streaming only"
        assert len(v["quality_levels"]) >= 2, "Must offer adaptive quality tiers for low bandwidth"


def test_get_videos_for_topic_alias():
    """Verify topic lookup works with curriculum topic alias (e.g. bio_10_ch01_t01)."""
    response = client.get("/v1/topics/bio_10_ch01_t01/videos")
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 2


def test_get_videos_with_language_filter():
    """Verify language-aware filtering for Telugu and English."""
    # Filter Telugu
    res_te = client.get("/v1/topics/bio_ch1_t1/videos?language=te")
    assert res_te.status_code == 200
    data_te = res_te.json()
    assert all(v["language_code"] == "te" for v in data_te["videos"])

    # Filter English
    res_en = client.get("/v1/topics/bio_ch1_t1/videos?language=en")
    assert res_en.status_code == 200
    data_en = res_en.json()
    assert all(v["language_code"] == "en" for v in data_en["videos"])


def test_get_video_details_by_id():
    """Verify fetching single video details and 404 for unknown video."""
    response = client.get("/v1/videos/vid_bio_ch1_t1_te")
    assert response.status_code == 200
    video = response.json()
    assert video["video_id"] == "vid_bio_ch1_t1_te"
    assert video["language_code"] == "te"
    assert video["online_streaming_only"] is True

    # Unknown video returns 404
    res_404 = client.get("/v1/videos/non_existent_video_id")
    assert res_404.status_code == 404


def test_get_unknown_topic_videos_returns_404():
    """Verify 404 for topic with no videos."""
    response = client.get("/v1/topics/unknown_topic_123/videos")
    assert response.status_code == 404


def test_chapter_package_includes_cached_video_metadata_without_media_blobs():
    """Phase 7 Exit Criterion 1: No video file is stored offline; metadata only in package."""
    response = client.get("/v1/curriculum/packages/biology/bio_ch1")
    assert response.status_code == 200
    pkg = response.json()

    cached_videos = pkg.get("cached_video_metadata", [])
    assert len(cached_videos) >= 2, "Package must contain cached video metadata for offline browsing"

    for v in cached_videos:
        assert "video_id" in v
        assert "title" in v
        assert "telugu_title" in v
        assert "duration_minutes" in v
        assert v.get("online_streaming_only") is True
        # Verify no binary media data is present
        assert "video_bytes" not in v
        assert "mp4_file" not in v


def test_video_watched_sync_event_awards_xp():
    """Phase 7 Scope: Video watched is recorded as a progress event."""
    payload = {
        "learner_id": "student_video_01",
        "device_id": "tablet_01",
        "events": [
            {
                "event_id": "evt_vid_001",
                "client_id": "tablet_01",
                "learner_id": "student_video_01",
                "event_type": "video_watched",
                "payload": {
                    "video_id": "vid_bio_ch1_t1_te",
                    "topic_id": "bio_ch1_t1",
                    "duration_seconds": 480,
                    "language": "te",
                },
                "timestamp": "2026-11-22T00:10:00Z",
            }
        ],
    }

    res = client.post("/v1/sync", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["processed_count"] == 1
    # 50 base XP + 15 XP for watching video = 65 XP
    assert data["progress"]["xp"] == 65
    assert data["progress"]["coins"] == 15
    assert "bio_ch1_t1" in data["progress"]["completed_topics"]

    # Replay batch to verify idempotency (Sync Rule 3)
    res_replay = client.post("/v1/sync", json=payload)
    assert res_replay.status_code == 200
    data_replay = res_replay.json()
    assert data_replay["processed_count"] == 0
    assert data_replay["duplicate_count"] == 1
    assert data_replay["progress"]["xp"] == 65
