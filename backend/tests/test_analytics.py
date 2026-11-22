"""Contract and Exit Criteria tests for Phase 9: Parent Dashboard and Analytics.

Exit Criteria [docs/implementationPlan.md: Phase 9]:
1. Dashboard values match the underlying progress records in test data.
2. Analytics endpoints serve time spent, weak areas, workbook completion rate, game performance, and gamification metrics.
3. Strict child privacy: zero chat transcripts exposed to parents.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_values_match_underlying_progress_records():
    """Exit Criterion: Dashboard values match the underlying progress records in test data."""
    learner_id = "test_parent_learner_1"

    # 1. Log an activity for this learner to establish underlying progress
    client.post(
        f"/v1/progress/{learner_id}/activity",
        json={"activity_type": "read_topic", "topic_id": "bio_ch1_t1"},
    )
    client.post(
        f"/v1/progress/{learner_id}/activity",
        json={"activity_type": "workbook", "topic_id": "bio_ch1_t1", "score": 90},
    )

    # 2. Fetch ground truth progress record
    prog_res = client.get(f"/v1/progress/{learner_id}")
    assert prog_res.status_code == 200
    prog_data = prog_res.json()

    # 3. Fetch Parent Analytics Dashboard
    analytics_res = client.get(f"/v1/analytics/parent/{learner_id}")
    assert analytics_res.status_code == 200
    analytics = analytics_res.json()

    # 4. Assert 100% fidelity between Dashboard values and underlying progress records
    assert analytics["learner_id"] == learner_id
    assert analytics["total_xp"] == prog_data["xp"], "Dashboard XP must match underlying progress record"
    assert analytics["current_level"] == prog_data["level"], "Dashboard Level must match underlying progress record"
    assert analytics["level_name"] == prog_data["level_name"], "Level title must match"
    assert analytics["learning_streak_days"] == prog_data["learning_streak_days"], "Streak must match"
    assert analytics["stars_earned"] == prog_data["stars"], "Stars must match"
    assert analytics["coins_earned"] == prog_data["coins"], "Coins must match"
    assert set(analytics["badges_earned"]) == set(prog_data["badges"]), "Badges must match"

    # Time spent and completion rates must be positive numbers
    assert analytics["total_time_spent_minutes"] > 0
    assert analytics["workbook_completion_rate"] >= 80.0
    assert analytics["game_performance_score"] >= 0.0


def test_weak_concepts_and_strength_areas():
    """Verify detection of weak concepts and strength areas."""
    learner_id = "test_parent_learner_2"

    # Topic 1: High score -> Strength Area
    client.post(
        f"/v1/progress/{learner_id}/activity",
        json={"activity_type": "workbook", "topic_id": "bio_ch1_t1", "score": 95},
    )

    # Topic 2: Low score -> Weak Concept
    client.post(
        f"/v1/progress/{learner_id}/activity",
        json={"activity_type": "workbook", "topic_id": "bio_ch1_t2", "score": 40},
    )

    analytics_res = client.get(f"/v1/analytics/parent/{learner_id}")
    assert analytics_res.status_code == 200
    data = analytics_res.json()

    # Verify Weak Concepts list contains topic with < 60% accuracy
    assert len(data["weak_concepts"]) >= 1
    weak = data["weak_concepts"][0]
    assert weak["accuracy_percentage"] < 60
    assert weak["recommended_action"] is not None
    assert weak["telugu_recommended_action"] is not None

    # Verify Strength Areas list contains high-performing topic
    assert len(data["strength_areas"]) >= 1
    strength = data["strength_areas"][0]
    assert strength["accuracy_percentage"] >= 80

    # Verify actionable improvement recommendations are provided in both languages
    assert len(data["improvement_recommendations"]) >= 2
    assert len(data["telugu_improvement_recommendations"]) >= 2


def test_minimum_data_notice_for_new_learner():
    """Verify minimum data notice is shown when learner has very few data points [Phase 9 Risk mitigation]."""
    learner_id = "brand_new_student_99"

    analytics_res = client.get(f"/v1/analytics/parent/{learner_id}")
    assert analytics_res.status_code == 200
    data = analytics_res.json()

    # As a new learner with < 2 activities, minimum_data_notice should be present
    assert data["minimum_data_notice"] is not None
    assert "Minimum data notice" in data["minimum_data_notice"]


def test_strict_child_privacy_no_chat_transcripts():
    """Verify strict child privacy: parents receive metrics only, ZERO chat transcripts [Arch: Parent visibility]."""
    learner_id = "privacy_test_learner"

    # Ask questions in chat
    client.post(
        "/v1/chat",
        json={"query": "What is Photosynthesis?", "language": "en", "class_name": "10"},
    )

    analytics_res = client.get(f"/v1/analytics/parent/{learner_id}")
    assert analytics_res.status_code == 200
    data = analytics_res.json()

    # Assert that no chat transcripts, messages, or conversation texts exist in response
    assert "chat_history" not in data
    assert "transcripts" not in data
    assert "messages" not in data
    assert "conversations" not in data
    assert "privacy_notice" in data
    assert "strictly private" in data["privacy_notice"].lower()


def test_parent_consent_and_pin_verification():
    """Verify parent account linking, consent storage, and PIN verification [R11]."""
    learner_id = "consent_test_learner"

    # 1. Register consent
    consent_payload = {
        "learner_id": learner_id,
        "parent_name": "Venkatesh Rao",
        "parent_contact": "venkat.rao@example.com",
        "consent_agreed": True,
        "pin_code": "5678",
    }
    consent_res = client.post("/v1/analytics/parent/consent", json=consent_payload)
    assert consent_res.status_code == 200
    consent_data = consent_res.json()
    assert consent_data["status"] == "linked"
    assert consent_data["parent_name"] == "Venkatesh Rao"
    assert consent_data["parent_id"].startswith("PAR-")

    # 2. Verify with correct PIN
    pin_ok_res = client.post(
        "/v1/analytics/parent/verify-pin",
        json={"learner_id": learner_id, "pin_code": "5678"},
    )
    assert pin_ok_res.status_code == 200
    assert pin_ok_res.json()["verified"] is True

    # 3. Verify with wrong PIN
    pin_fail_res = client.post(
        "/v1/analytics/parent/verify-pin",
        json={"learner_id": learner_id, "pin_code": "0000"},
    )
    assert pin_fail_res.status_code == 200
    assert pin_fail_res.json()["verified"] is False
