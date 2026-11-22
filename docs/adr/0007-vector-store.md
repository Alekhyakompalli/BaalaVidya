# ADR 0007: Vector store for ingestion and dev (qdrant-client local mode)

## Status

Accepted for Phase 1 ingestion and local development. Provisional for the Railway deployment (see Phase 2A).

## Context

ADR 0006 and Phase 0 set up a Qdrant dev container via `infra/dev/docker-compose.yml`. Docker is not installed on the development machine, so the container cannot run. Phase 1 needs a vector index now.

## Decision

Use `qdrant-client` in local (embedded) mode, with the store at `ingestion/data/qdrant_local`. No Qdrant server is needed for Phase 1. The docker-compose file is kept for later use.

## Consequences

Phase 1 indexing and tests run without Docker. Local mode is single-process and is not for production or concurrent access. Phase 2A still needs a server-hosted Qdrant on Railway or Qdrant Cloud, and that choice remains open. The on-disk store is generated data and is excluded from git by `ingestion/data/` in `.gitignore`. The same client code should work against a server URL later, so only the client constructor changes.

## Revisit-by

Phase 2A (before Railway deployment).
