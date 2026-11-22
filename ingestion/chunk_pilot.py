r"""Phase 1 chunking for the English-medium Class 10 pilot PDFs (no OCR).

Run command (from the repository root):
    ingestion\.venv\Scripts\python.exe ingestion\chunk_pilot.py

Reads the pilot PDFs in data/raw/class 10, splits each page into sentence-packed
chunks with a small overlap, and writes one JSON record per chunk to
data/chunks/class10_pilot.jsonl.
"""

import hashlib
import json
import re
import uuid
from pathlib import Path

import pymupdf

RAW = Path(__file__).resolve().parent / "data" / "raw" / "class 10"
PILOT = [
    {"file": "X Mathematics EM  2026-27.pdf", "subject": "Mathematics", "medium": "EM"},
    {"file": "x biology em inner 2026-27.pdf", "subject": "Biology", "medium": "EM"},
]
OUT = Path(__file__).resolve().parent / "data" / "chunks" / "class10_pilot.jsonl"
NAMESPACE = uuid.UUID("6f1c2a52-4b9e-4d1a-9c3e-2b7a1f0d5e10")
TARGET_CHARS = 900
OVERLAP_CHARS = 120
MIN_CHARS = 80

BLOCK_SIZE = 1024 * 1024  # 1 MiB


def file_sha256(path):
    """Return the hex SHA-256 of a file, streamed in 1 MiB blocks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(BLOCK_SIZE)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def page_texts(doc):
    """Return (1-based page number, normalised text) for pages with enough text."""
    out = []
    for page_number in range(1, doc.page_count + 1):
        raw = doc.load_page(page_number - 1).get_text("text")
        text = re.sub(r"\s+", " ", raw).strip()
        if len(text) < MIN_CHARS:
            continue
        out.append((page_number, text))
    return out


def chapter_map(doc):
    """Map page numbers to chapter labels from level-1 TOC entries.

    Only level-1 entries with page >= 1 are used. Each title becomes a label:
    a trailing ".pdf" is removed; "Initial Page(s)" becomes "" (front matter);
    "Lesson N" / "LessonN" / "Lesson-N" becomes "Lesson N"; a bare number N
    becomes "Chapter N"; anything else is kept as the stripped title.
    Each entry covers from its page up to the page before the next valid entry
    (the last one runs to the end of the document). Pages before the first
    valid entry, and pages whose label is "", are left out of the result, so
    callers should fall back to "" for them.
    """
    def label_for(title):
        name = re.sub(r"\.pdf$", "", title.strip(), flags=re.IGNORECASE).strip()
        if re.match(r"^Initial Pages?\.?$", name, flags=re.IGNORECASE):
            return ""
        lesson = re.match(r"^Lesson[- ]?(\d+)$", name, flags=re.IGNORECASE)
        if lesson:
            return "Lesson " + str(int(lesson.group(1)))
        if re.match(r"^\d+$", name):
            return "Chapter " + str(int(name))
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



def _hard_split(sentence):
    """Split a sentence longer than TARGET_CHARS into TARGET_CHARS pieces."""
    if len(sentence) <= TARGET_CHARS:
        return [sentence]
    return [sentence[i:i + TARGET_CHARS] for i in range(0, len(sentence), TARGET_CHARS)]


def _overlap_tail(text):
    """Return the last OVERLAP_CHARS characters of text, without a partial first word."""
    if len(text) <= OVERLAP_CHARS:
        return text.strip()
    tail = text[-OVERLAP_CHARS:]
    if " " in tail:
        tail = tail.split(" ", 1)[1]
    else:
        tail = ""
    return tail.strip()


def chunk_page_text(text):
    """Pack sentences into chunks of up to TARGET_CHARS with OVERLAP_CHARS carry-over."""
    pieces = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        sentence = sentence.strip()
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
        return chunks
    return [chunk for chunk in chunks if len(chunk) >= MIN_CHARS]


def chunk_id(source_sha, page, index, text):
    """Deterministic chunk ID derived from source hash, location and text hash."""
    text_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return str(uuid.uuid5(NAMESPACE, f"{source_sha}:{page}:{index}:{text_sha}"))


def _build(entry):
    """Return (records, pages_with_text, chapters_detected) for one PILOT entry."""
    path = RAW / entry["file"]
    source_sha = file_sha256(path)
    records = []
    with pymupdf.open(path) as doc:
        chapters = chapter_map(doc)
        chapters_detected = sum(1 for level, _, _ in doc.get_toc(simple=True) if level == 1)
        pages = page_texts(doc)

    for page_number, text in pages:
        chapter = chapters.get(page_number, "")
        for index, chunk in enumerate(chunk_page_text(text)):
            records.append({
                "chunk_id": chunk_id(source_sha, page_number, index, chunk),
                "class": "10",
                "subject": entry["subject"],
                "medium": entry["medium"],
                "language": "en",
                "chapter": chapter,
                "topic": "",
                "source_file": entry["file"],
                "source_sha256": source_sha,
                "source_page": page_number,
                "chunk_index": index,
                "text": chunk,
            })
    return records, len(pages), chapters_detected


def build_records(entry):
    """Return the chunk records for one PILOT entry."""
    return _build(entry)[0]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(OUT, "w", encoding="utf-8", newline="\n") as out:
        for entry in PILOT:
            records, pages_with_text, chapters_detected = _build(entry)
            for record in records:
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
            total += len(records)
            print(f"{entry['file']}: pages_with_text={pages_with_text} "
                  f"chunks={len(records)} chapters_detected={chapters_detected}")
    print(f"TOTAL chunks={total} -> {OUT}")


if __name__ == "__main__":
    main()
