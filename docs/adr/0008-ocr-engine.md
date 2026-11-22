# ADR 0008: OCR engine for scanned and font-encoded pages (Tesseract)

## Status

Accepted (confirmed by R7 quality check across 70 pilot pages; see `docs/eval-results/r7_ocr_quality.md`)

## Context

The Telugu-medium SCERT PDFs have no Unicode Telugu text layer (using legacy 8-bit custom font encodings), so native PDF text extraction yields non-Unicode characters. Phase 1 requires OCR for Telugu content (R7). The architecture originally suggested Azure Document Intelligence (cloud API). We evaluated Tesseract v5.4.0 with Telugu trained data (`tel.traineddata` from `tessdata_best`) rendered at 300 DPI via PyMuPDF.

## Decision

Use Tesseract OCR with `tel.traineddata` and PyMuPDF 300 DPI rendering (`zoom = 300/72`), cached to local disk (`ingestion/data/ocr_cache`).

Empirical evidence from R7 quality evaluation (`docs/eval-results/r7_ocr_quality.md`):
- **Analyzed:** 70 pilot pages across Biology TM (Lessons 1 & 2) and Telugu First Language (Lessons 01–03).
- **Extraction Success:** 100% (0 blank/failed pages).
- **Telugu Script Density:** 83.2% of extracted non-whitespace characters are valid Telugu Unicode (`\u0C00-\u0C7F`).
- **Domain Term Recognition:** Complex conjuncts such as `కిరణజన్య సంయోగక్రియ`, `శ్వాసక్రియ`, `హరితరేణువు`, `మైటోకాండ్రియా`, and `రక్త ప్రసరణ` extracted intact and accurately searchable.
- **Retrieval Performance:** Achieved 100% Recall@5 on curated syllabus queries and 93.8% Recall@5 across all sampled Telugu queries.

## Consequences

- No Azure Document Intelligence API key, cloud network calls, or subscription costs are required for Phase 1.
- Ingestion pipeline is reproducible offline.
- Caching extracted page text in `ocr_cache` ensures deterministic, instantaneous subsequent pipeline runs.

## Revisit-by

Phase 5 (when assessing OCR pipelines for additional classes beyond the pilot).
