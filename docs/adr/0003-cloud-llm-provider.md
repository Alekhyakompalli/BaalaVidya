# ADR 0003: Cloud LLM provider (R3)

## Status

Provisional (to be confirmed in Phase 1 / Phase 5 evidence)

## Context

R3 in `docs/architecture.md`. The cloud LLM answers when the device is online (LLM routing).

## Decision

Provisional choice: Azure OpenAI, the same vendor as Azure Document Intelligence used for OCR.

Alternative: GPT API direct.

Confirm with cost, Telugu answer quality and child-data terms (R11) before Phase 2.

## Consequences

One vendor for LLM and OCR keys. Keys are held as environment variables only.

Revisit-by: before Phase 2.
