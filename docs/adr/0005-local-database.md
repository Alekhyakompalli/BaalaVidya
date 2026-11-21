# ADR 0005: Local database (Flutter client)

## Status

Provisional

## Context

`docs/architecture.md` leaves the local database library open. The on-device store holds syllabus data, progress and a sync queue (Offline store and sync).

## Decision

Drift on SQLite (`drift` and `sqlite3_flutter_libs`).

## Consequences

`client/pubspec.yaml` includes both `drift` and `sqlite3_flutter_libs`.

Revisit-by: Phase 5.
