"""Progress and Gamification API routes."""

from fastapi import APIRouter

from app.schemas.progress import (
    ActivityLogRequest,
    CertificateGenerationRequest,
    CertificateResponse,
    MissionChallengeRequest,
    MissionChallengeResponse,
    PersonalizedPracticeRequest,
    PersonalizedPracticeResponse,
    ProgressResponse,
    UnlockableItem,
)
from app.services.progress_service import (
    delete_learner_progress,
    evaluate_mission_challenge,
    generate_certificate,
    generate_personalized_practice,
    get_learner_progress,
    log_activity,
)

router = APIRouter(prefix="/v1/progress", tags=["Progress & Gamification"])


@router.get("/{learner_id}", response_model=ProgressResponse)
def get_progress(learner_id: str):
    """Get learning progress, streak, questions asked, badges, level and topic mastery for a student."""
    return get_learner_progress(learner_id)


@router.post("/{learner_id}/activity", response_model=ProgressResponse)
def record_activity(learner_id: str, request: ActivityLogRequest):
    """Log completion of a workbook, quiz, game, or reading session and award XP/mastery."""
    return log_activity(learner_id, request)


@router.post("/{learner_id}/personalized-practice", response_model=PersonalizedPracticeResponse)
def request_personalized_practice(learner_id: str, request: PersonalizedPracticeRequest):
    """Generate simplified analogies and booster exercises when a student struggles with a topic [PS: 11]."""
    return generate_personalized_practice(request)


@router.post("/{learner_id}/certificate", response_model=CertificateResponse)
def issue_certificate(learner_id: str, request: CertificateGenerationRequest):
    """Generate and store an official Achievement Certificate for a completed chapter [PS: 11]."""
    return generate_certificate(learner_id, request)


@router.get("/{learner_id}/certificates", response_model=list[CertificateResponse])
def get_certificates(learner_id: str):
    """List all achievement certificates earned by a learner."""
    progress = get_learner_progress(learner_id)
    return progress.certificates


@router.get("/{learner_id}/unlockables", response_model=list[UnlockableItem])
def get_unlockables(learner_id: str):
    """List unlockable learning games, badges, and themes [PS: 11. Progress-based Unlockables]."""
    progress = get_learner_progress(learner_id)
    unlocked = set(progress.unlocked_items)

    return [
        UnlockableItem(
            item_id="game_bio_01",
            title="Photosynthesis Chef Game",
            telugu_title="కిరణజన్య సంయోగక్రియ చెఫ్",
            item_type="game",
            is_unlocked="game_bio_01" in unlocked,
            required_xp=0,
        ),
        UnlockableItem(
            item_id="game_mission_challenge",
            title="Chapter 1 Mission Challenge",
            telugu_title="1వ అధ్యాయం మిషన్ ఛాలెంజ్",
            item_type="game",
            is_unlocked="game_mission_challenge" in unlocked or progress.xp >= 100,
            required_xp=100,
        ),
        UnlockableItem(
            item_id="theme_galaxy",
            title="Cosmic Explorer Avatar & Theme",
            telugu_title="కాస్మిక్ ఎక్స్‌ప్లోరర్ థీమ్",
            item_type="theme",
            is_unlocked="theme_galaxy" in unlocked or progress.xp >= 200,
            required_xp=200,
        ),
    ]


@router.post("/{learner_id}/mission-challenge", response_model=MissionChallengeResponse)
def submit_mission_challenge(learner_id: str, request: MissionChallengeRequest):
    """Submit end-of-chapter Mission Challenge combining quiz, puzzle, scenario, and mini game [PS: 11]."""
    return evaluate_mission_challenge(learner_id, request)


@router.delete("/{learner_id}")
def delete_progress(learner_id: str):
    """Permanently delete all learning progress records for a student [Right to be Forgotten - ADR 0012]."""
    deleted = delete_learner_progress(learner_id)
    return {"status": "purged", "learner_id": learner_id, "deleted": deleted}
