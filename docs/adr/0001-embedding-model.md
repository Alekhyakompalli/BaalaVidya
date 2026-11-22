# ADR 0001: Embedding model (R1)

## Status

Accepted (confirmed by Phase 1 empirical evaluation on real SCERT chunks)

## Context

R1 in `docs/architecture.md` (Key risks), Phase 1 of `docs/implementationPlan.md`, and `docs/eval.md`.
Telugu and English retrieval quality on real SCERT content was measured across 1,822 textbook chunks and a bilingual query set to compare `intfloat/multilingual-e5-base` and `BAAI/bge-m3`. Full report in `docs/eval-results/r1_bilingual.md`.

## Decision

Accept `intfloat/multilingual-e5-base` as the primary embedding model for both Telugu and English curriculum content.

Empirical evaluation evidence:
- **Telugu Recall@5:** 93.8% (identical to `BAAI/bge-m3` at 93.8%)
- **English Recall@5:** 88.7% across full evaluation set (100.0% on curated core syllabus queries)
- **Vector Dimension:** 768 (vs. 1024 for `bge-m3`, 25% lower vector storage)
- **Encoding Latency:** 495.7 seconds (3.4x faster than `bge-m3` at 1693.5 seconds)
- **Model Size:** ~1.1 GB (vs. ~2.2 GB for `bge-m3`, 50% lower memory footprint)

## Consequences

- Vector store collections use vector dimension 768 and Cosine distance metric.
- `pilot_chunks` collection in Qdrant is populated with 768-dimensional embeddings of all pilot chapters.
- The 768-dim model size fits well within resource budgets for server hosting and offline/on-device packages.
- Both Telugu and English queries require prefix `query: ` during search, and documents require prefix `passage: ` during indexing.

## Revisit-by

Phase 5 (when packaging the offline on-device index, to confirm device RAM footprint).
