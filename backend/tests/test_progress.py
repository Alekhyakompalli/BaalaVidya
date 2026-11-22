"""Contract tests for Progress API service."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_progress():
    response = client.get("/v1/progress/learner_alpha")
    assert response.status_code == 200
    data = response.json()
    assert data["learner_id"] == "learner_alpha"
    assert "xp" in data
    assert "coins" in data
    assert "stars" in data
    assert "learning_streak_days" in data
    assert "mastery_levels" in data


def test_log_activity_increases_xp():
    learner = "learner_beta"
    initial = client.get(f"/v1/progress/{learner}").json()["xp"]

    payload = {
        "activity_type": "quiz",
        "topic_id": "bio_10_ch01_t01",
        "score": 100,
    }
    response = client.post(f"/v1/progress/{learner}/activity", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["xp"] > initial
    assert data["stars"] >= 1
