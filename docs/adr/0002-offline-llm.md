# ADR 0002: Offline on-device LLM (R2)

## Status

Provisional (to be confirmed in Phase 1 / Phase 5 evidence)

## Context

R2 in `docs/architecture.md`. The on-device model must run on low-resource devices (Arch: Deployment and runtime considerations).

## Decision

Provisional choice: Gemma 2B.

Alternative: Phi-3 Mini.

Confirm with on-device size and latency measurement in Phase 5 on the lowest-spec target device.

## Consequences

Model size drives the app package size and the device minimum spec.

Revisit-by: Phase 5.
