# ADR 0006: Repository layout and route prefixes

## Status

Provisional

## Context

Phase 0 of `docs/implementationPlan.md`.

## Decision

Folders:

- `client/` (Flutter)
- `backend/` (FastAPI)
- `ingestion/` (Phase 1 pipeline)
- `docs/`
- `infra/dev/` (Qdrant dev container via docker compose)
- `.github/workflows/` (CI)

Route prefixes proposed in `docs/architecture.md`:

- `/v1/classes`
- `/v1/search`
- `/v1/chat`
- `/v1/progress`
- `/v1/sync`
- `/v1/analytics`

## Consequences

Folder names are proposed, not sourced. Revisit-by: Phase 2.
