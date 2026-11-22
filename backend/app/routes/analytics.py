"""Analytics and Parent Dashboard API routes.

Adheres to:
- [PS: 10. Parent Dashboard; Parent Insights]
- [Arch: Parent visibility; Child privacy R11; Analytics service]
- [ADR 0011: Parent Dashboard, Analytics & Child Privacy Architecture]
"""

from fastapi import APIRouter

from app.schemas.analytics import (
    ParentConsentRequest,
    ParentConsentResponse,
    ParentDashboardResponse,
    ParentPinVerificationRequest,
    ParentPinVerificationResponse,
)
from app.services.analytics_service import (
    delete_parent_and_learner_data,
    get_parent_analytics,
    link_parent_account,
    verify_parent_pin,
)

router = APIRouter(prefix="/v1/analytics", tags=["Analytics & Parent Dashboard"])


@router.get("/parent/{learner_id}", response_model=ParentDashboardResponse)
def get_parent_dashboard(learner_id: str):
    """Retrieve parent dashboard metrics: time spent, weak areas, workbook completion, and gamification."""
    return get_parent_analytics(learner_id)


@router.post("/parent/consent", response_model=ParentConsentResponse)
def register_parent_consent(request: ParentConsentRequest):
    """Link parent account to child profile and record parental consent [Arch: Recommendations R11]."""
    return link_parent_account(request)


@router.post("/parent/verify-pin", response_model=ParentPinVerificationResponse)
def check_parent_pin(request: ParentPinVerificationRequest):
    """Verify parental gate PIN before accessing Parent Dashboard on shared devices."""
    return verify_parent_pin(request)


@router.delete("/parent/{learner_id}/data")
def delete_student_and_parent_data(learner_id: str):
    """Permanently delete all student telemetry, progress, and parent links [Right to be Forgotten - ADR 0012]."""
    return delete_parent_and_learner_data(learner_id)
