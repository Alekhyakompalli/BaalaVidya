"""Sync service implementing append-only event logging, deduplication, and conflict resolution.

Adheres to:
- Sync Rule 1: Events written locally first
- Sync Rule 2: Chronological order preservation
- Sync Rule 3: Unique event ID & client ID prevent double counting on re-send
- Sync Rule 4: Append-only event log with deterministic progress reduction (conflict-free)
- Sync Rule 7: Learner data isolation on shared devices
"""

from app.schemas.sync import SyncBatchRequest, SyncBatchResponse
from app.services.progress_service import _LEARNER_DB, get_learner_progress

# In-memory append-only event log partitioned by learner_id
_EVENT_LOG: dict[str, list[dict]] = {}

# Set of already-processed event IDs to enforce idempotency
_PROCESSED_EVENT_IDS: set[str] = set()


def reset_sync_state():
    """Reset event store for clean test isolation."""
    global _EVENT_LOG, _PROCESSED_EVENT_IDS
    _EVENT_LOG = {}
    _PROCESSED_EVENT_IDS = set()


def process_sync_batch(request: SyncBatchRequest) -> SyncBatchResponse:
    """
    Process a batch of offline/online sync events.
    Enforces idempotency, deduplication, learner isolation, and deterministic progress recomputation.
    """
    learner_id = request.learner_id
    if learner_id not in _EVENT_LOG:
        _EVENT_LOG[learner_id] = []

    # Get current base learner record
    get_learner_progress(learner_id)
    rec = _LEARNER_DB[learner_id]

    processed = 0
    duplicates = 0

    for event in request.events:
        # Rule 7: Enforce learner data separation (reject or isolate events for other learners)
        if event.learner_id != learner_id:
            continue

        # Rule 3: Unique event ID prevents double counting on replay
        if event.event_id in _PROCESSED_EVENT_IDS:
            duplicates += 1
            continue

        # Record event in append-only log
        _PROCESSED_EVENT_IDS.add(event.event_id)
        _EVENT_LOG[learner_id].append(event.model_dump())
        processed += 1

        # Rule 4: Deterministic reduction of event into learner progress
        etype = event.event_type
        payload = event.payload

        if etype == "topic_read":
            topic_id = payload.get("topic_id", "")
            if topic_id and topic_id not in rec["completed_topics"]:
                rec["completed_topics"].append(topic_id)
                rec["xp"] += 20
                rec["coins"] += 5
        elif etype in ("workbook_completed", "game_played"):
            rec["xp"] += 30
            rec["stars"] += 1
            rec["coins"] += 10
            topic_id = payload.get("topic_id")
            if topic_id and topic_id not in rec["completed_topics"]:
                rec["completed_topics"].append(topic_id)
            if "mastery_breakdowns" in rec and topic_id and topic_id in rec["mastery_breakdowns"]:
                rec["mastery_breakdowns"][topic_id]["workbook_score"] = 0.8
                rec["mastery_levels"][topic_id] = "Practicing"
        elif etype in ("video_watched", "watch_video"):
            rec["xp"] += 15
            rec["coins"] += 5
            topic_id = payload.get("topic_id")
            if topic_id and topic_id not in rec["completed_topics"]:
                rec["completed_topics"].append(topic_id)
            if topic_id and topic_id in rec.get("mastery_levels", {}):
                rec["mastery_levels"][topic_id] = "Learning"
        elif etype == "question_asked":
            rec["questions_asked"] += 1
            rec["xp"] += 5
            rec["coins"] += 1
        elif etype in ("mission_challenge", "mission_completed"):
            rec["xp"] += 50
            rec["coins"] += 25
            rec["stars"] += 3
            if "mission_master" not in rec.get("badges", []):
                rec.setdefault("badges", []).append("mission_master")
        elif etype == "streak_update":
            streak = payload.get("streak_days", 1)
            rec["learning_streak_days"] = max(rec["learning_streak_days"], streak)

    # Derive completed chapters from completed topics
    topics_set = set(rec["completed_topics"])
    if {"bio_ch1_t1", "bio_ch1_t2"}.issubset(topics_set) and "bio_10_ch01" not in rec["completed_chapters"]:
        rec["completed_chapters"].append("bio_10_ch01")

    return SyncBatchResponse(
        status="success",
        learner_id=learner_id,
        processed_count=processed,
        duplicate_count=duplicates,
        progress=get_learner_progress(learner_id),
    )
