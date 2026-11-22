"""Bilingual curriculum ingestion pipeline for Class 10 pilot.

Supports both direct PDF text extraction (for English-medium books) and
OCR extraction with caching (for Telugu-medium books).
Outputs deterministic, metadata-tagged chunks to data/chunks/class10_pilot.jsonl.
"""

import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pymupdf
from ingestion.ocr import extract_page_text

RAW = Path(__file__).resolve().parent / "data" / "raw" / "class 10"
OUT = Path(__file__).resolve().parent / "data" / "chunks" / "class10_pilot.jsonl"
NAMESPACE = uuid.UUID("6f1c2a52-4b9e-4d1a-9c3e-2b7a1f0d5e10")

TARGET_CHARS = 900
OVERLAP_CHARS = 120
MIN_CHARS = 80
BLOCK_SIZE = 1024 * 1024  # 1 MiB

PILOT_CONFIG = [
    {
        "file": "X Mathematics EM  2026-27.pdf",
        "subject": "Mathematics",
        "medium": "EM",
        "language": "en",
        "is_telugu": False,
        "page_range": None,  # all pages
    },
    {
        "file": "x biology em inner 2026-27.pdf",
        "subject": "Biology",
        "medium": "EM",
        "language": "en",
        "is_telugu": False,
        "page_range": None,  # all pages
    },
    {
        "file": "X Biology TM Inner 2026-27.pdf",
        "subject": "Biology",
        "medium": "TM",
        "language": "te",
        "is_telugu": True,
        "page_range": range(11, 61),  # Lesson 1 (pages 11-35) and Lesson 2 (pages 36-60)
    },
    {
        "file": "10th Telugu OM Inner Pages 2026-27.pdf",
        "subject": "Telugu",
        "medium": "TM",
        "language": "te",
        "is_telugu": True,
        "page_range": range(12, 32),  # Lessons 01-03 (pages 12-31)
    },
]


def file_sha256(path: Path) -> str:
    """Return the hex SHA-256 of a file, streamed in 1 MiB blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(BLOCK_SIZE)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def chapter_map(doc: pymupdf.Document) -> dict[int, str]:
    """Map page numbers to chapter labels from level-1 TOC entries."""
    def label_for(title: str) -> str:
        name = re.sub(r"\.pdf$", "", title.strip(), flags=re.IGNORECASE).strip()
        if re.match(r"^Initial Pages?\.?$", name, flags=re.IGNORECASE):
            return ""
        lesson = re.match(r"^Lesson[- ]?(\d+)$", name, flags=re.IGNORECASE)
        if lesson:
            return "Lesson " + str(int(lesson.group(1)))
        chapt = re.match(r"^(\d+)\s*chapt", name, flags=re.IGNORECASE)
        if chapt:
            return "Chapter " + str(int(chapt.group(1)))
        if re.match(r"^\d+$", name):
            return "Chapter " + str(int(name))
        lessons = re.match(r"^\d+\.\s*(lessons\s*\d+[-–]\d+)", name, flags=re.IGNORECASE)
        if lessons:
            return lessons.group(1).title()
        return name

    toc = doc.get_toc(simple=True)
    starts = [(page, label_for(title))
              for level, title, page in toc if level == 1 and page >= 1]
    starts.sort(key=lambda entry: entry[0])
    result = {}
    for idx, (start, label) in enumerate(starts):
        if idx + 1 < len(starts):
            end = starts[idx + 1][0] - 1
        else:
            end = doc.page_count
        if not label:
            continue
        for page_number in range(start, end + 1):
            result[page_number] = label
    return result


def _hard_split(sentence: str) -> list[str]:
    """Split a sentence longer than TARGET_CHARS into TARGET_CHARS pieces."""
    if len(sentence) <= TARGET_CHARS:
        return [sentence]
    return [sentence[i:i + TARGET_CHARS] for i in range(0, len(sentence), TARGET_CHARS)]


def _overlap_tail(text: str) -> str:
    """Return the last OVERLAP_CHARS characters of text, without a partial first word."""
    if len(text) <= OVERLAP_CHARS:
        return text.strip()
    tail = text[-OVERLAP_CHARS:]
    if " " in tail:
        tail = tail.split(" ", 1)[1]
    else:
        tail = ""
    return tail.strip()


def chunk_page_text(text: str) -> list[str]:
    """Pack sentences into chunks of up to TARGET_CHARS with OVERLAP_CHARS carry-over."""
    pieces = []
    # Split across English (.!?) and Indic/Telugu (।॥) sentence terminators and linebreaks
    for sentence in re.split(r"(?<=[.!?।॥])\s+|\n{2,}", text):
        sentence = re.sub(r"\s+", " ", sentence).strip()
        if sentence:
            pieces.extend(_hard_split(sentence))

    chunks = []
    current = ""
    for piece in pieces:
        if not current:
            current = piece
        elif len(current) + 1 + len(piece) <= TARGET_CHARS:
            current += " " + piece
        else:
            chunks.append(current)
            tail = _overlap_tail(current)
            if tail and len(tail) + 1 + len(piece) <= TARGET_CHARS:
                current = tail + " " + piece
            else:
                current = piece
    if current:
        chunks.append(current)

    if len(chunks) == 1:
        return [chunks[0]] if len(chunks[0]) >= MIN_CHARS else []
    return [chunk for chunk in chunks if len(chunk) >= MIN_CHARS]


def chunk_id(source_sha: str, page: int, index: int, text: str) -> str:
    """Deterministic chunk ID derived from source hash, location and text hash."""
    text_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return str(uuid.uuid5(NAMESPACE, f"{source_sha}:{page}:{index}:{text_sha}"))


def process_entry(entry: dict) -> tuple[list[dict], int, int]:
    """Extract, chunk, and tag chunks for one textbook entry."""
    path = RAW / entry["file"]
    if not path.exists():
        for subfolder in ["English medium", "Telugu medium"]:
            alt_path = RAW / subfolder / entry["file"]
            if alt_path.exists():
                path = alt_path
                break
    if not path.exists():
        print(f"[Warning] File not found: {path}")
        return [], 0, 0

    source_sha = file_sha256(path)
    records = []
    pages_processed = 0

    with pymupdf.open(path) as doc:
        chapters = chapter_map(doc)
        chapters_detected = len(set(chapters.values()))

        page_range = entry.get("page_range") or range(1, doc.page_count + 1)
        for page_number in page_range:
            if page_number < 1 or page_number > doc.page_count:
                continue

            text = extract_page_text(doc, page_number, entry["file"], is_telugu_pdf=entry["is_telugu"])
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) < MIN_CHARS:
                continue

            pages_processed += 1
            chapter = chapters.get(page_number, "")
            chunks = chunk_page_text(text)

            for index, chunk in enumerate(chunks):
                cid = chunk_id(source_sha, page_number, index, chunk)
                records.append({
                    "chunk_id": cid,
                    "class": "10",
                    "subject": entry["subject"],
                    "medium": entry["medium"],
                    "language": entry["language"],
                    "chapter": chapter,
                    "topic": "",
                    "source_file": entry["file"],
                    "source_sha256": source_sha,
                    "source_page": page_number,
                    "chunk_index": index,
                    "text": chunk,
                })

    return records, pages_processed, chapters_detected


def run_pipeline(output_path: Path = OUT) -> list[dict]:
    """Run full ingestion pipeline and write records to JSONL."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    all_records = []

    print("=== Running Curriculum Ingestion Pipeline ===")
    with open(output_path, "w", encoding="utf-8", newline="\n") as out_fh:
        for entry in PILOT_CONFIG:
            print(f"Processing {entry['file']} ({entry['subject']} {entry['medium']})...")
            records, pages_count, chapters_count = process_entry(entry)
            for rec in records:
                out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            all_records.extend(records)
            print(f"  -> Extracted {pages_count} pages, {len(records)} chunks, {chapters_count} chapters.")

    print(f"\nPipeline complete: {len(all_records)} total chunks written to {output_path}")
    return all_records


if __name__ == "__main__":
    run_pipeline()
