# BAALAVIDYA

BAALAVIDYA is a bilingual (Telugu and English) learning app for children in Classes 1 to 10, built around SCERT syllabus content with an AI tutor. Design: docs/architecture.md. Plan: docs/implementationPlan.md.

## Repository layout

- `client/` : Flutter app
- `backend/` : FastAPI service
- `ingestion/` : curriculum ingestion pipeline (Phase 1)
- `docs/` : architecture, plan, ADRs in `docs/adr/`
- `infra/dev/` : dev Qdrant container (`docker-compose.yml`)
- `.github/workflows/` : CI

## Run locally

- Qdrant: `docker compose -f infra/dev/docker-compose.yml up -d`
- Backend tests: from `backend/`, `python -m pytest`
- Client tests: from `client/`, `flutter test`

## Environment variables (names only; never commit values)

- `CLOUD_LLM_API_KEY`
- `AZURE_DOCUMENT_INTELLIGENCE_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
