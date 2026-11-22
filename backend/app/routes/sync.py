"""Sync API routes."""

from fastapi import APIRouter

from app.schemas.sync import SyncBatchRequest, SyncBatchResponse
from app.services.sync_service import process_sync_batch

router = APIRouter(prefix="/v1/sync", tags=["Sync"])


@router.post("", response_model=SyncBatchResponse)
def sync_events(request: SyncBatchRequest):
    """
    Sync progress events from client devices.
    - Idempotent: replayed batches leave totals unchanged.
    - Conflict-free: out-of-order device batches produce identical final state.
    - Isolated: strictly separates learner data on shared devices.
    """
    return process_sync_batch(request)
