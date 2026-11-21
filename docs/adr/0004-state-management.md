# ADR 0004: State management (Flutter client)

## Status

Provisional

## Context

`docs/architecture.md` leaves the state-management library open (Flutter client section).

## Decision

Riverpod (`flutter_riverpod`).

Reason: state logic is testable without a BuildContext.

## Consequences

`client/pubspec.yaml` depends on `flutter_riverpod`. Screens read providers.

Revisit-by: Phase 3.
