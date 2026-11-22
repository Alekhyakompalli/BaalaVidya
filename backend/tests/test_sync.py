"""Contract and concurrency tests for Phase 6 Sync and Cloud Progress.

Verifies:
- Exit Criterion 1: A replayed batch leaves totals unchanged (idempotency).
- Exit Criterion 2: Two devices that both record events for one learner produce the same totals regardless of sync order.
- Unique client ID / event ID prevents double counting.
- Learner separation on shared devices (Sync Rule 7).
- Progress endpoints reflect synced progress.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.progress_service import _LEARNER_DB
from app.services.sync_service import reset_sync_state

client = TestClient(app)


def setup_function():
    """Reset in-memory state before each test."""
    reset_sync_state()
    _LEARNER_DB.clear()


def test_single_device_sync_processes_events():
    """Verify batch sync updates learner progress."""
    payload = {
        "learner_id": "student_sync_1",
        "device_id": "device_mobile_1",
        "events": [
            {
                "event_id": "evt_001",
                "client_id": "device_mobile_1",
                "learner_id": "student_sync_1",
                "event_type": "topic_read",
                "payload": {"topic_id": "bio_ch1_t1"},
                "timestamp": "2026-11-22T00:00:00Z",
            },
            {
                "event_id": "evt_002",
                "client_id": "device_mobile_1",
                "learner_id": "student_sync_1",
                "event_type": "workbook_completed",
                "payload": {"activity_id": "wb_01", "topic_id": "bio_ch1_t1"},
                "timestamp": "2026-11-22T00:05:00Z",
            },
        ],
    }

    res = client.post("/v1/sync", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["processed_count"] == 2
    assert data["duplicate_count"] == 0
    assert "bio_ch1_t1" in data["progress"]["completed_topics"]
    assert data["progress"]["xp"] == 100  # 50 base + 20 read + 30 workbook


def test_replayed_batch_leaves_totals_unchanged():
    """Phase 6 Exit Criterion 1: A replayed batch leaves totals unchanged."""
    payload = {
        "learner_id": "student_idempotency",
        "device_id": "device_tablet_1",
        "events": [
            {
                "event_id": "evt_idem_1",
                "client_id": "device_tablet_1",
                "learner_id": "student_idempotency",
                "event_type": "topic_read",
                "payload": {"topic_id": "bio_ch1_t1"},
                "timestamp": "2026-11-22T00:01:00Z",
            },
            {
                "event_id": "evt_idem_2",
                "client_id": "device_tablet_1",
                "learner_id": "student_idempotency",
                "event_type": "question_asked",
                "payload": {"query": "What is Photosynthesis?"},
                "timestamp": "2026-11-22T00:02:00Z",
            },
        ],
    }

    # First Send
    res1 = client.post("/v1/sync", json=payload)
    assert res1.status_code == 200
    initial_progress = res1.json()["progress"]
    assert res1.json()["processed_count"] == 2

    # Replay Exact Same Batch
    res2 = client.post("/v1/sync", json=payload)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["processed_count"] == 0
    assert data2["duplicate_count"] == 2

    # Exit Criterion: Totals must be IDENTICAL after replay
    replayed_progress = data2["progress"]
    assert initial_progress["xp"] == replayed_progress["xp"]
    assert initial_progress["completed_topics"] == replayed_progress["completed_topics"]
    assert initial_progress["questions_asked"] == replayed_progress["questions_asked"]
    assert initial_progress["coins"] == replayed_progress["coins"]
    assert initial_progress["stars"] == replayed_progress["stars"]


def test_two_device_sync_gives_identical_totals_regardless_of_order():
    """Phase 6 Exit Criterion 2: Two devices syncing out of order produce identical final totals."""
    device_a_batch = [
        {
            "event_id": "evt_devA_1",
            "client_id": "device_A",
            "learner_id": "student_crdt",
            "event_type": "topic_read",
            "payload": {"topic_id": "bio_ch1_t1"},
            "timestamp": "2026-11-22T00:01:00Z",
        },
        {
            "event_id": "evt_devA_2",
            "client_id": "device_A",
            "learner_id": "student_crdt",
            "event_type": "workbook_completed",
            "payload": {"activity_id": "wb_bio_01", "topic_id": "bio_ch1_t1"},
            "timestamp": "2026-11-22T00:03:00Z",
        },
    ]

    device_b_batch = [
        {
            "event_id": "evt_devB_1",
            "client_id": "device_B",
            "learner_id": "student_crdt",
            "event_type": "topic_read",
            "payload": {"topic_id": "bio_ch1_t2"},
            "timestamp": "2026-11-22T00:02:00Z",
        },
        {
            "event_id": "evt_devB_2",
            "client_id": "device_B",
            "learner_id": "student_crdt",
            "event_type": "question_asked",
            "payload": {"query": "What is respiration?"},
            "timestamp": "2026-11-22T00:04:00Z",
        },
    ]

    # --- Scenario 1: Device A syncs first, then Device B ---
    reset_sync_state()
    _LEARNER_DB.clear()

    client.post("/v1/sync", json={"learner_id": "student_crdt", "device_id": "device_A", "events": device_a_batch})
    res_ab = client.post("/v1/sync", json={"learner_id": "student_crdt", "device_id": "device_B", "events": device_b_batch})
    totals_order_ab = res_ab.json()["progress"]

    # --- Scenario 2: Device B syncs first, then Device A ---
    reset_sync_state()
    _LEARNER_DB.clear()

    client.post("/v1/sync", json={"learner_id": "student_crdt", "device_id": "device_B", "events": device_b_batch})
    res_ba = client.post("/v1/sync", json={"learner_id": "student_crdt", "device_id": "device_A", "events": device_a_batch})
    totals_order_ba = res_ba.json()["progress"]

    # Exit Criterion: Totals must be identical for both sync orders
    assert totals_order_ab["xp"] == totals_order_ba["xp"]
    assert set(totals_order_ab["completed_topics"]) == set(totals_order_ba["completed_topics"])
    assert totals_order_ab["questions_asked"] == totals_order_ba["questions_asked"]
    assert totals_order_ab["coins"] == totals_order_ba["coins"]
    assert totals_order_ab["stars"] == totals_order_ba["stars"]
    assert set(totals_order_ab["completed_chapters"]) == set(totals_order_ba["completed_chapters"])


def test_learner_separation_on_shared_device():
    """Sync Rule 7: Events for learner 1 must never affect learner 2 on shared devices."""
    batch_l1 = {
        "learner_id": "learner_alekhya",
        "device_id": "shared_tablet_01",
        "events": [
            {
                "event_id": "evt_l1_1",
                "client_id": "shared_tablet_01",
                "learner_id": "learner_alekhya",
                "event_type": "topic_read",
                "payload": {"topic_id": "bio_ch1_t1"},
                "timestamp": "2026-11-22T00:01:00Z",
            }
        ],
    }

    batch_l2 = {
        "learner_id": "learner_ravi",
        "device_id": "shared_tablet_01",
        "events": [
            {
                "event_id": "evt_l2_1",
                "client_id": "shared_tablet_01",
                "learner_id": "learner_ravi",
                "event_type": "question_asked",
                "payload": {"query": "What is chlorophyll?"},
                "timestamp": "2026-11-22T00:02:00Z",
            }
        ],
    }

    client.post("/v1/sync", json=batch_l1)
    client.post("/v1/sync", json=batch_l2)

    p1 = client.get("/v1/progress/learner_alekhya").json()
    p2 = client.get("/v1/progress/learner_ravi").json()

    # Learner 1 has topic completed but 0 questions asked
    assert "bio_ch1_t1" in p1["completed_topics"]
    assert p1["questions_asked"] == 0

    # Learner 2 has question asked but 0 completed topics
    assert len(p2["completed_topics"]) == 0
    assert p2["questions_asked"] == 1


def test_progress_endpoint_matches_synced_state():
    """Verify GET /v1/progress/{learner_id} returns all required fields."""
    client.post(
        "/v1/sync",
        json={
            "learner_id": "student_endpoint_test",
            "device_id": "device_1",
            "events": [
                {
                    "event_id": "evt_ep_1",
                    "client_id": "device_1",
                    "learner_id": "student_endpoint_test",
                    "event_type": "topic_read",
                    "payload": {"topic_id": "bio_ch1_t1"},
                    "timestamp": "2026-11-22T00:01:00Z",
                }
            ],
        },
    )

    res = client.get("/v1/progress/student_endpoint_test")
    assert res.status_code == 200
    p = res.json()
    assert "completed_topics" in p
    assert "completed_chapters" in p
    assert "questions_asked" in p
    assert "learning_streak_days" in p
    assert "xp" in p
    assert "coins" in p
    assert "stars" in p
