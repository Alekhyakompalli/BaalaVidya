"""Pydantic schemas for Analytics service and Parent Dashboard.

Adheres to:
- [PS: 10. Parent Dashboard; Parent Insights]
- [Arch: Parent visibility; Child privacy R11; Analytics service]
- [ADR 0011: Parent Dashboard, Analytics & Child Privacy Architecture]
"""

from pydantic import BaseModel, Field


class ParentConsentRequest(BaseModel):
    learner_id: str
    parent_name: str
    parent_contact: str = Field(..., description="Email or phone number of parent")
    consent_agreed: bool = True
    pin_code: str = Field("1234", description="4-digit PIN for parent zone access")


class ParentConsentResponse(BaseModel):
    status: str = "linked"
    parent_id: str
    learner_id: str
    parent_name: str
    consent_agreed: bool
    linked_at: str


class ParentPinVerificationRequest(BaseModel):
    learner_id: str
    pin_code: str


class ParentPinVerificationResponse(BaseModel):
    verified: bool
    message: str


class SubjectProgressSummary(BaseModel):
    subject_id: str
    subject_name: str
    telugu_subject_name: str
    completed_topics_count: int
    total_topics_count: int
    time_spent_minutes: int
    completion_percentage: int


class ConceptInsight(BaseModel):
    topic_id: str
    topic_title: str
    telugu_topic_title: str
    subject_id: str
    accuracy_percentage: int
    status: str = Field("needs_practice", description="'weak' | 'needs_practice' | 'strength'")
    recommended_action: str
    telugu_recommended_action: str
    has_sufficient_data: bool = True


class ParentDashboardResponse(BaseModel):
    learner_id: str
    learner_name: str
    total_time_spent_minutes: int
    time_spent_today_minutes: int
    subjects_completed_count: int
    subjects_in_progress_count: int
    subject_summaries: list[SubjectProgressSummary]

    # Workbook & Game Performance
    workbook_completion_rate: float = Field(..., description="Percentage of workbooks completed (0-100)")
    workbooks_completed_count: int
    game_performance_score: float = Field(..., description="Average game score (0-100)")
    games_completed_count: int

    # Concept Insights & Recommendations
    weak_concepts: list[ConceptInsight]
    strength_areas: list[ConceptInsight]
    improvement_recommendations: list[str]
    telugu_improvement_recommendations: list[str]
    minimum_data_notice: str | None = None

    # Gamification Metrics
    total_xp: int
    current_level: int
    level_name: str
    learning_streak_days: int
    badges_earned: list[str]
    stars_earned: int
    coins_earned: int

    # Child Privacy Assurance [Arch: Parent visibility]
    privacy_notice: str = "Child chat conversations are strictly private to support pressure-free learning curiosity."
