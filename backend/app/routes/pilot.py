"""Pilot evaluation and stakeholder feedback API routes.

Adheres to:
- [PS: Success Metrics 1 to 6]
- [Plan: Phase 11 Pilot Scope and Exit Criteria]
- [ADR 0013: Pilot Evaluation, Success Metrics & Launch Architecture]
"""

from fastapi import APIRouter

from app.schemas.pilot import (
    PilotFeedbackRequest,
    PilotFeedbackResponse,
    PilotFeedbackSummary,
    PilotMetricsSummaryResponse,
)
from app.services.pilot_service import (
    get_pilot_feedback_summary,
    get_pilot_metrics_summary,
    submit_pilot_feedback,
)

router = APIRouter(prefix="/v1/pilot", tags=["Pilot, Beta & Launch"])


@router.get("/metrics", response_model=PilotMetricsSummaryResponse)
def get_metrics():
    """Retrieve official measured values against agreed product owner targets for all 6 Success Metrics."""
    return get_pilot_metrics_summary()


@router.post("/feedback", response_model=PilotFeedbackResponse)
def post_feedback(request: PilotFeedbackRequest):
    """Submit student, teacher, parent, or volunteer pilot feedback."""
    return submit_pilot_feedback(request)


@router.get("/feedback/summary", response_model=PilotFeedbackSummary)
def get_feedback_summary():
    """Retrieve aggregated stakeholder feedback statistics and key themes."""
    return get_pilot_feedback_summary()
