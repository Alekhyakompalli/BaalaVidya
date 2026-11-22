"""Script to OCR selected Telugu pilot chapters and cache them.

Processes:
1. X Biology TM Inner 2026-27.pdf: Lesson 1 (pages 11-35) and Lesson 2 (pages 36-60)
2. 10th Telugu OM Inner Pages 2026-27.pdf: Lessons 01-03 (pages 12-42)

Caches text in ingestion/data/ocr_cache so re-runs are instant.
"""

import os
import sys
import time
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.ocr import extract_page_text, OCR_CACHE
import pymupdf

RAW = Path(__file__).resolve().parent / "data" / "raw" / "class 10"

TARGETS = [
    {
        "file": "X Biology TM Inner 2026-27.pdf",
        "pages": range(11, 36),  # Lesson 1 (pages 11-35)
        "subject": "Biology",
        "medium": "TM",
    },
    {
        "file": "X Biology TM Inner 2026-27.pdf",
        "pages": range(36, 61),  # Lesson 2 (pages 36-60)
        "subject": "Biology",
        "medium": "TM",
    },
    {
        "file": "10th Telugu OM Inner Pages 2026-27.pdf",
        "pages": range(12, 32),  # Lessons 01-03 first part (pages 12-31)
        "subject": "Telugu",
        "medium": "TM",
    }
]


def run_ocr_pilot():
    OCR_CACHE.mkdir(parents=True, exist_ok=True)
    total_pages = sum(len(t["pages"]) for t in TARGETS)
    print(f"Starting OCR for {total_pages} pilot Telugu pages...")
    start_time = time.time()
    processed = 0

    for target in TARGETS:
        pdf_path = RAW / target["file"]
        if not pdf_path.exists():
            print(f"[Warning] {pdf_path} not found!")
            continue
        doc = pymupdf.open(pdf_path)
        print(f"\nProcessing {target['file']} ({target['subject']}) pages {list(target['pages'])[0]}-{list(target['pages'])[-1]}...")
        for pno in target["pages"]:
            t0 = time.time()
            text = extract_page_text(doc, pno, target["file"], is_telugu_pdf=True)
            elapsed = time.time() - t0
            tel_count = sum(1 for c in text if 0x0C00 <= ord(c) <= 0x0C7F)
            processed += 1
            print(f"  [{processed}/{total_pages}] Page {pno:03d}: len={len(text)} telugu_chars={tel_count} in {elapsed:.1f}s")
        doc.close()

    total_time = time.time() - start_time
    print(f"\nCompleted OCR for {processed} pages in {total_time:.1f} seconds ({total_time/max(processed, 1):.1f}s/page).")


if __name__ == "__main__":
    run_ocr_pilot()
