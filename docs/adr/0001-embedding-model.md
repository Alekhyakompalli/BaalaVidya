# ADR 0001: Embedding model (R1)

## Status

Provisional (to be confirmed in Phase 1 / Phase 5 evidence)

## Context

R1 in `docs/architecture.md` (Key risks) and Phase 0 of `docs/implementationPlan.md`. Telugu and English retrieval quality on SCERT content must be measured before the embedding model is locked in.

## Decision

Provisional choice: `multilingual-e5-base`.

Alternative: BGE-M3.

Confirm with the Phase 1 embedding comparison on real SCERT Telugu and English chunks.

## Consequences

The embedding model and vector size are fixed for Phase 1 indexing. Changing it later means re-embedding all chunks.

Revisit-by: end of Phase 1.
