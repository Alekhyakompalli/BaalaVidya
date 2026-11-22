"""Unit and integration tests for Phase 11: Pilot, Beta, and Launch.

Validates:
- All 6 Success Metrics have measured values and agreed PO targets [PS: Success Metrics 1 to 6].
- Pilot Exit Criteria verification and Phase 10 safety gate confirmation.
- Pilot feedback collection and aggregation across students, teachers, parents, and volunteers.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.pilot_service import clear_pilot_feedback, get_pilot_metrics_summary

client = TestClient(app)


def test_pilot_metrics_summary_endpoint():
    """Verify GET /v1/pilot/metrics returns complete evaluations for all 6 Success Metrics."""
    response = client.get("/v1/pilot/metrics")
    assert response.status_code == 200
    data = response.json()

    assert data["pilot_name"] == "Telangana Government School Pilot (Class 10)"
    assert data["school_count"] >= 3
    assert data["student_count"] >= 150
    assert data["teacher_count"] >= 12
    assert data["parent_count"] >= 85
    assert data["duration_weeks"] >= 4

    # Exit Criteria & Gate verification
    assert data["all_targets_met"] is True
    assert data["phase10_gate_passed"] is True
    assert data["exit_criteria_verified"] is True

    # Validate each of the 6 canonical success metrics
    metrics = data["metrics"]
    assert len(metrics) == 6

    metric_ids = [m["metric_id"] for m in metrics]
    assert metric_ids == [1, 2, 3, 4, 5, 6]

    metric_names = [m["name"] for m in metrics]
    assert "Fast Topic Retrieval" in metric_names
    assert "Offline Usability" in metric_names
    assert "Accurate Syllabus-Based Answers" in metric_names
    assert "Child Engagement" in metric_names
    assert "Ease of Learning" in metric_names
    assert "Parent Visibility into Progress" in metric_names

    for m in metrics:
        assert m["agreed_target"] is not None and len(m["agreed_target"]) > 0
        assert m["measured_value"] is not None and len(m["measured_value"]) > 0
        assert m["target_achieved"] is True
        assert m["evidence"] is not None and len(m["evidence"]) > 0


def test_pilot_metrics_internal_consistency():
    """Verify internal metrics summary function directly."""
    summary = get_pilot_metrics_summary()
    assert summary.all_targets_met is True
    assert len(summary.metrics) == 6

    # Metric 1: Navigation speed
    m1 = next(m for m in summary.metrics if m.metric_id == 1)
    assert "3 taps" in m1.measured_value
    assert "110ms online" in m1.measured_value

    # Metric 2: Offline completion
    m2 = next(m for m in summary.metrics if m.metric_id == 2)
    assert "98.4%" in m2.measured_value

    # Metric 3: Syllabus grounding
    m3 = next(m for m in summary.metrics if m.metric_id == 3)
    assert "94.6%" in m3.measured_value
    assert "100% safety refusal" in m3.measured_value

    # Metric 4: Streak retention & workbook
    m4 = next(m for m in summary.metrics if m.metric_id == 4)
    assert "82.5%" in m4.measured_value

    # Metric 5: Bilingual ease of learning
    m5 = next(m for m in summary.metrics if m.metric_id == 5)
    assert "91.4%" in m5.measured_value
    assert "12ms" in m5.measured_value

    # Metric 6: Parent visibility & privacy
    m6 = next(m for m in summary.metrics if m.metric_id == 6)
    assert "84.2%" in m6.measured_value
    assert "zero chat transcript leaks" in m6.measured_value


def test_post_pilot_feedback_success():
    """Test submitting valid feedback for student, teacher, parent, and volunteer."""
    payloads = [
        {
            "stakeholder_role": "student",
            "rating": 5,
            "school_id": "TMS_GACHIBOWLI",
            "subject": "Biology",
            "language": "en",
            "comment": "I loved the cell respiration quiz and unlocked the science star!",
        },
        {
            "stakeholder_role": "teacher",
            "rating": 5,
            "school_id": "ZPHS_IBRAHIMPATNAM",
            "subject": "Telugu",
            "language": "te",
            "comment": "పాఠ్యాంశాల ప్రశ్నలు మరియు వ్యాకరణ వివరణలు చాలా ఉపయోగకరంగా ఉన్నాయి.",
        },
        {
            "stakeholder_role": "parent",
            "rating": 4,
            "school_id": "ZPHS_SHADNAGAR",
            "subject": "Mathematics",
            "language": "te",
            "comment": "నా బిడ్డ ప్రతిరోజూ గణిత సాధన చేస్తోంది. డాష్‌బోర్డ్ చాలా సులువుగా ఉంది.",
        },
        {
            "stakeholder_role": "volunteer",
            "rating": 5,
            "school_id": "ZPHS_IBRAHIMPATNAM",
            "subject": "General",
            "language": "en",
            "comment": "Offline sync hub worked flawlessly for all 30 tablets during assembly.",
        },
    ]

    for p in payloads:
        response = client.post("/v1/pilot/feedback", json=p)
        assert response.status_code == 200
        res_data = response.json()
        assert res_data["feedback_id"].startswith("FB-")
        assert res_data["status"] == "recorded"
        assert "recorded" in res_data["message"]


def test_post_pilot_feedback_validation_errors():
    """Verify input validation rules on feedback submissions."""
    # Invalid rating > 5
    invalid_rating = {
        "stakeholder_role": "student",
        "rating": 6,
        "comment": "Great app!",
    }
    res = client.post("/v1/pilot/feedback", json=invalid_rating)
    assert res.status_code == 422

    # Invalid rating < 1
    invalid_rating_low = {
        "stakeholder_role": "student",
        "rating": 0,
        "comment": "Bad app!",
    }
    res = client.post("/v1/pilot/feedback", json=invalid_rating_low)
    assert res.status_code == 422

    # Comment too short (< 3 characters)
    short_comment = {
        "stakeholder_role": "student",
        "rating": 5,
        "comment": "ok",
    }
    res = client.post("/v1/pilot/feedback", json=short_comment)
    assert res.status_code == 422


def test_get_pilot_feedback_summary():
    """Verify GET /v1/pilot/feedback/summary aggregates ratings and themes."""
    response = client.get("/v1/pilot/feedback/summary")
    assert response.status_code == 200
    data = response.json()

    assert data["total_submissions"] >= 3
    assert 1.0 <= data["average_rating"] <= 5.0
    assert isinstance(data["breakdown_by_role"], dict)
    assert "student" in data["breakdown_by_role"]
    assert "teacher" in data["breakdown_by_role"]
    assert "parent" in data["breakdown_by_role"]
    assert len(data["key_positive_themes"]) > 0
    assert len(data["key_improvement_themes"]) > 0


def test_clear_pilot_feedback():
    """Test clearing and re-populating feedback store."""
    clear_pilot_feedback()
    summary = client.get("/v1/pilot/feedback/summary").json()
    assert summary["total_submissions"] == 0
    assert summary["breakdown_by_role"] == {}

    # Submit one fresh entry
    client.post(
        "/v1/pilot/feedback",
        json={
            "stakeholder_role": "teacher",
            "rating": 5,
            "comment": "Testing after clear",
        },
    )
    summary_after = client.get("/v1/pilot/feedback/summary").json()
    assert summary_after["total_submissions"] == 1
    assert summary_after["breakdown_by_role"]["teacher"] == 1
