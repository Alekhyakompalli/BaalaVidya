"""Logging and retention policy service for BAALAVIDYA [ADR 0012].

Implements:
1. PII sanitization (phone numbers, email addresses, Indian Aadhaar numbers, IP masking)
2. 30-day retention limit on telemetry logs
3. Zero chat transcript persistence policy (R11 & Arch: Child Privacy)
"""

import re
from datetime import UTC, datetime, timedelta
from typing import Any

# In-memory structured telemetry event log
_TELEMETRY_LOGS: list[dict[str, Any]] = []

PHONE_REGEX = re.compile(r"(?:\+?91[\s-]?)?[6-9]\d{9}")
EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}")
AADHAAR_REGEX = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")
IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def sanitize_text(text: str) -> str:
    """Mask any PII found in log texts (phone, email, Aadhaar, IP)."""
    if not text:
        return text
    sanitized = PHONE_REGEX.sub("[REDACTED_PHONE]", text)
    sanitized = EMAIL_REGEX.sub("[REDACTED_EMAIL]", sanitized)
    sanitized = AADHAAR_REGEX.sub("[REDACTED_AADHAAR]", sanitized)
    sanitized = IP_REGEX.sub("0.0.0.0", sanitized)
    return sanitized


def sanitize_telemetry_event(event: dict[str, Any]) -> dict[str, Any]:
    """Sanitize a telemetry event before storage.

    Guarantees:
    - Zero chat transcripts or raw student question text stored
    - IP addresses masked to 0.0.0.0
    - PII scrubbed
    """
    clean_event = {}
    for k, v in event.items():
        # Do not persist raw queries or transcripts to permanent log
        if k in ("query", "text", "message", "transcript", "raw_query"):
            clean_event[k] = "[QUERY_REDACTED_FOR_CHILD_PRIVACY]"
        elif isinstance(v, str):
            clean_event[k] = sanitize_text(v)
        elif isinstance(v, dict):
            clean_event[k] = sanitize_telemetry_event(v)
        else:
            clean_event[k] = v

    if "timestamp" not in clean_event:
        clean_event["timestamp"] = datetime.now(UTC).isoformat()

    return clean_event


def record_telemetry_event(event: dict[str, Any]) -> dict[str, Any]:
    """Record sanitized telemetry event and enforce retention."""
    clean = sanitize_telemetry_event(event)
    _TELEMETRY_LOGS.append(clean)
    prune_expired_logs(max_days=30)
    return clean


def prune_expired_logs(max_days: int = 30) -> int:
    """Enforce 30-day retention limit by removing logs older than max_days.

    Returns count of pruned records.
    """
    cutoff = datetime.now(UTC) - timedelta(days=max_days)
    initial_count = len(_TELEMETRY_LOGS)

    surviving = []
    for log in _TELEMETRY_LOGS:
        ts_str = log.get("timestamp")
        if ts_str:
            try:
                dt = datetime.fromisoformat(ts_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=UTC)
                if dt >= cutoff:
                    surviving.append(log)
            except (ValueError, TypeError):
                surviving.append(log)
        else:
            surviving.append(log)

    _TELEMETRY_LOGS[:] = surviving
    return initial_count - len(surviving)


def get_telemetry_logs() -> list[dict[str, Any]]:
    """Return all active sanitized telemetry logs."""
    prune_expired_logs(max_days=30)
    return list(_TELEMETRY_LOGS)


def clear_all_telemetry_logs() -> None:
    """Purge all stored telemetry logs."""
    _TELEMETRY_LOGS.clear()
