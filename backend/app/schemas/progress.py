"""Progress and Gamification Pydantic schemas.

Adheres to:
- [PS: 9. Learning Progress]
- [PS: 11. Play & Learn Module; Learning Rewards; Topic Mastery Score; End-of-Chapter Challenge]
- [Arch: Gamification engine; R8 Mastery and XP formulas]
- [ADR 0010: Gamification, Mastery Formulas & Play and Learn Specification]
"""

from typing import Any

from pydantic import BaseModel, Field


class MasteryBreakdown(BaseModel):
    reading_score: float = Field(0.0, description="0.0 to 1.0 reading completion")
    workbook_score: float = Field(0.0, description="0.0 to 1.0 workbook accuracy")
    quiz_score: float = Field(0.0, description="0.0 to 1.0 quiz score")
    game_score: float = Field(0.0, description="0.0 to 1.0 game accuracy")
    ai_score: float = Field(0.0, description="0.0 to 1.0 AI doubts asked")
    total_score: float = Field(0.0, description="0.0 to 100.0 weighted score")
    level: str = Field("Beginner", description="Beginner, Learning, Practicing, Mastered")


class CertificateResponse(BaseModel):
    certificate_id: str
    learner_id: str
    learner_name: str
    subject_id: str
    chapter_id: str
    chapter_title: str
    telugu_chapter_title: str
    score_percentage: int
    issue_date: str
    badge_name: str
    verified_by: str = "Bala Buddy Official Tutor"


class CertificateGenerationRequest(BaseModel):
    chapter_id: str
    learner_name: str = "Student"
    score_percentage: int = 100


class UnlockableItem(BaseModel):
    item_id: str
    title: str
    telugu_title: str
    item_type: str  # 'game', 'theme', 'badge', 'certificate'
    is_unlocked: bool = True
    required_xp: int = 0


class PersonalizedExercise(BaseModel):
    exercise_id: str
    question: str
    telugu_question: str
    options: list[str]
    telugu_options: list[str]
    correct_index: int
    simplified_hint: str
    telugu_simplified_hint: str


class PersonalizedPracticeRequest(BaseModel):
    topic_id: str
    subject_id: str = "biology"
    current_score_percentage: int = 40
    language: str = "en"


class PersonalizedPracticeResponse(BaseModel):
    topic_id: str
    struggling_detected: bool
    encouragement_message: str
    simplified_explanation: str
    telugu_simplified_explanation: str
    extra_exercises: list[PersonalizedExercise]


class MissionChallengeRequest(BaseModel):
    chapter_id: str
    quiz_score: int
    puzzle_solved: bool
    scenario_answered: bool
    mini_game_score: int


class MissionChallengeResponse(BaseModel):
    chapter_id: str
    completed: bool
    earned_xp: int
    earned_coins: int
    earned_badge: str
    certificate_id: str | None = None
    feedback: str
    telugu_feedback: str


class ProgressResponse(BaseModel):
    learner_id: str
    completed_topics: list[str] = []
    completed_chapters: list[str] = []
    questions_asked: int = 0
    learning_streak_days: int = 1
    xp: int = 0
    coins: int = 0  # Reconciled 1 Coin = 1 Learning Point
    stars: int = 0
    level: int = 1
    level_name: str = "Curious Scout"
    badges: list[str] = Field(default_factory=list, description="Earned badges collection")
    unlocked_items: list[str] = Field(default_factory=list, description="Unlocked games, themes, and challenges")
    certificates: list[CertificateResponse] = Field(default_factory=list, description="Earned achievement certificates")
    mastery_levels: dict[str, str] = Field(default_factory=dict, description="Topic ID to mastery label")
    mastery_breakdowns: dict[str, MasteryBreakdown] = Field(
        default_factory=dict, description="Topic ID to detailed mastery calculation"
    )


class ActivityLogRequest(BaseModel):
    activity_type: str = Field(
        ...,
        description="E.g. 'read_topic', 'workbook', 'quiz', 'game', 'question_asked', 'mission_challenge'",
    )
    topic_id: str
    score: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
