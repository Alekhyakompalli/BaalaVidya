"""Schemas for Phase 11: Pilot, Beta and Launch.

Adheres to:
- [PS: Success Metrics 1 to 6]
- [Plan: Phase 11 Pilot Scope and Exit Criteria]
- [ADR 0013: Pilot Evaluation, Success Metrics & Launch Architecture]
"""

from pydantic import BaseModel, Field


class SuccessMetricEvaluation(BaseModel):
    metric_id: int
    name: str
    description: str
    agreed_target: str
    measured_value: str
    target_achieved: bool
    evidence: str


class PilotMetricsSummaryResponse(BaseModel):
    pilot_name: str
    school_count: int
    student_count: int
    teacher_count: int
    parent_count: int
    duration_weeks: int
    metrics: list[SuccessMetricEvaluation]
    all_targets_met: bool
    phase10_gate_passed: bool
    exit_criteria_verified: bool


class PilotFeedbackRequest(BaseModel):
    stakeholder_role: str = Field(..., description="Role: 'student', 'teacher', 'parent', or 'volunteer'")
    rating: int = Field(..., ge=1, le=5, description="Satisfaction score from 1 to 5")
    school_id: str | None = Field(default=None, description="School identifier or district")
    subject: str | None = Field(default=None, description="Subject reviewed: Biology, Math, Telugu")
    language: str = Field(default="en", description="Language: 'en' or 'te'")
    comment: str = Field(..., min_length=3, description="Feedback or suggestion")


class PilotFeedbackResponse(BaseModel):
    feedback_id: str
    status: str
    received_at: str
    message: str


class PilotFeedbackSummary(BaseModel):
    total_submissions: int
    average_rating: float
    breakdown_by_role: dict[str, int]
    key_positive_themes: list[str]
    key_improvement_themes: list[str]
