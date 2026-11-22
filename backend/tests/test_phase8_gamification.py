"""Contract and Exit Criteria tests for Phase 8: Progress, Gamification, and Play & Learn.

Exit Criteria [docs/implementationPlan.md: Phase 8]:
1. Mastery and XP match a hand-computed sample.
2. Activities complete offline and sync later.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.progress_service import (
    calculate_topic_mastery,
    get_learner_level,
)

client = TestClient(app)


def test_hand_computed_mastery_sample():
    """Exit Criterion 1: Mastery matches hand-computed sample on fixed inputs.

    Hand-computed calculation from ADR 0010:
    Weights: R=0.20, W=0.30, Q=0.20, G=0.20, A=0.10
    Input: R=1.0, W=0.8, Q=0.9, G=0.7, A=0.5
    S = (0.20*1.0 + 0.30*0.8 + 0.20*0.9 + 0.20*0.7 + 0.10*0.5) * 100
      = (0.20 + 0.24 + 0.18 + 0.14 + 0.05) * 100
      = 0.81 * 100 = 81.0% -> Level = 'Practicing'
    """
    score, level = calculate_topic_mastery(
        reading=1.0,
        workbook=0.8,
        quiz=0.9,
        game=0.7,
        ai_doubts=0.5,
    )
    assert score == 81.0, f"Expected 81.0, got {score}"
    assert level == "Practicing", f"Expected Practicing, got {level}"


def test_hand_computed_mastery_boundaries():
    """Test boundary conditions for all 4 mastery levels: Beginner, Learning, Practicing, Mastered."""
    # 1. Beginner: < 30
    score, level = calculate_topic_mastery(reading=0.5, workbook=0.0, quiz=0.0, game=0.0, ai_doubts=0.0)
    assert score == 10.0
    assert level == "Beginner"

    # 2. Learning: 30 <= score < 60
    score, level = calculate_topic_mastery(reading=1.0, workbook=0.5, quiz=0.5, game=0.0, ai_doubts=0.0)
    assert score == 45.0
    assert level == "Learning"

    # 3. Practicing: 60 <= score < 85
    score, level = calculate_topic_mastery(reading=1.0, workbook=0.8, quiz=0.8, game=0.5, ai_doubts=0.0)
    # (0.20*1.0 + 0.30*0.8 + 0.20*0.8 + 0.20*0.5) * 100 = (0.20 + 0.24 + 0.16 + 0.10)*100 = 70.0
    assert score == 70.0
    assert level == "Practicing"

    # 4. Mastered: >= 85
    score, level = calculate_topic_mastery(reading=1.0, workbook=1.0, quiz=1.0, game=1.0, ai_doubts=1.0)
    assert score == 100.0
    assert level == "Mastered"


def test_xp_formula_and_level_thresholds():
    """Verify XP calculation and level thresholds match ADR 0010."""
    assert get_learner_level(50) == (1, "Curious Scout 🌱")
    assert get_learner_level(99) == (1, "Curious Scout 🌱")
    assert get_learner_level(100) == (2, "Eager Explorer 🚀")
    assert get_learner_level(199) == (2, "Eager Explorer 🚀")
    assert get_learner_level(250) == (3, "Knowledge Seeker 📚")
    assert get_learner_level(380) == (4, "Rising Scholar 💡")
    assert get_learner_level(520) == (6, "Master Learner 🏆")


def test_log_activity_updates_mastery_and_xp():
    """Verify logging activities properly awards XP, coins, stars, and upgrades mastery level."""
    learner = "phase8_student_1"

    # Log topic reading
    res1 = client.post(
        f"/v1/progress/{learner}/activity",
        json={"activity_type": "read_topic", "topic_id": "bio_ch1_t1"},
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert "bio_ch1_t1" in data1["completed_topics"]
    assert data1["xp"] >= 70

    # Log workbook completion with high score
    res2 = client.post(
        f"/v1/progress/{learner}/activity",
        json={"activity_type": "workbook", "topic_id": "bio_ch1_t1", "score": 90},
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["xp"] > data1["xp"]
    assert data2["stars"] >= 3
    assert data2["coins"] > data1["coins"]
    # Check mastery level upgraded
    assert data2["mastery_levels"]["bio_ch1_t1"] in ("Learning", "Practicing")


def test_personalized_practice_generation():
    """Verify AI-generated personalized practice for struggling learners [PS: 11]."""
    payload = {
        "topic_id": "bio_ch1_t1",
        "subject_id": "biology",
        "current_score_percentage": 40,
        "language": "en",
    }
    response = client.post("/v1/progress/phase8_student_2/personalized-practice", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["struggling_detected"] is True
    assert "simplified_explanation" in data
    assert "telugu_simplified_explanation" in data
    assert len(data["extra_exercises"]) >= 2
    assert "encouragement_message" in data


def test_achievement_certificate_generation():
    """Verify certificate generation and retrieval [PS: 11; Arch: Gamification engine]."""
    learner = "phase8_student_3"
    payload = {
        "chapter_id": "bio_ch1",
        "learner_name": "Ravi Kumar",
        "score_percentage": 95,
    }
    response = client.post(f"/v1/progress/{learner}/certificate", json=payload)
    assert response.status_code == 200
    cert = response.json()
    assert cert["certificate_id"].startswith("CERT-BIO_CH1")
    assert cert["learner_name"] == "Ravi Kumar"
    assert "Nutrition" in cert["chapter_title"]

    # Retrieve certificates list
    list_res = client.get(f"/v1/progress/{learner}/certificates")
    assert list_res.status_code == 200
    certs = list_res.json()
    assert len(certs) >= 1
    assert certs[0]["certificate_id"] == cert["certificate_id"]


def test_unlockables_api():
    """Verify progress-based unlockables [PS: 11. Progress-based Unlockables]."""
    learner = "phase8_student_4"
    res = client.get(f"/v1/progress/{learner}/unlockables")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 2
    assert any(i["item_id"] == "game_bio_01" for i in items)


def test_mission_challenge_evaluation():
    """Verify End-of-Chapter Mission Challenge completion and badge reward [PS: 11]."""
    learner = "phase8_student_5"
    payload = {
        "chapter_id": "bio_ch1",
        "quiz_score": 90,
        "puzzle_solved": True,
        "scenario_answered": True,
        "mini_game_score": 85,
    }
    res = client.post(f"/v1/progress/{learner}/mission-challenge", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["completed"] is True
    assert data["earned_xp"] == 50
    assert data["earned_badge"] == "mission_master"
    assert data["certificate_id"] is not None

    # Check that learner's progress reflects the mission completion
    prog_res = client.get(f"/v1/progress/{learner}")
    prog = prog_res.json()
    assert "mission_master" in prog["badges"]
    assert "bio_ch1" in prog["completed_chapters"]
