"""Extract lesson text from textbook PDFs into topic JSON files.

Reads ingestion/data/raw/class N/<medium folder>/*.pdf and writes
ingestion/data/topics/class{N}/{subject}_{medium}.json
(one JSON list of chapter records per class, subject and medium).
"""
import json
import os
import re
from pathlib import Path

from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
RAW_DIR = BASE / "data" / "raw"
TOPICS_DIR = BASE / "data" / "topics"

HEADING_RE = re.compile(
    r"^(lesson|chapter|unit|పాఠం)\s*[-:]?\s*(\d+|[IVX]+)\b\s*[-:.]?\s*(.*)$",
    re.IGNORECASE,
)
PAGE_NUMBER_RE = re.compile(r"^(page\s*)?\d{1,4}$", re.IGNORECASE)
EXERCISE_RE = re.compile(r"^(exercise|activity|answer the following|note)\s*:?$", re.IGNORECASE)
SENTENCE_END_RE = re.compile(r"[.?!।](?=\s|$)")
SUBJECT_RULES = [
    (("physics",), "Physics"),
    (("biology",), "Biology"),
    (("chem",), "Chemistry"),
    (("maths", "mathematics", "math"), "Mathematics"),
    (("science",), "General Science"),
    (("social", "gs"), "Social Studies"),
    (("english", "reader"), "English"),
    (("telugu", "fl", "om"), "Telugu"),
    (("sanskrit", "san_"), "Sanskrit"),
]
MIN_BODY_CHARS = 200
MAX_EXPLANATION = 4000


def subject_from_name(filename):
    name = filename.lower()
    for keywords, subject in SUBJECT_RULES:
        if any(k in name for k in keywords):
            return subject
    return "Other"


def class_and_medium(pdf):
    """Class number from the 'class N' folder; medium from the immediate folder name."""
    class_num = None
    for part in pdf.relative_to(RAW_DIR).parts[:-1]:
        m = re.search(r"class\s*(\d+)", part, re.IGNORECASE)
        if m:
            class_num = int(m.group(1))
    medium = "te" if "telugu" in pdf.parent.name.lower() else "en"
    return class_num, medium


def clean_lines(reader):
    """Return (page_no, text) pairs with whitespace normalised; blanks and bare page numbers dropped."""
    lines = []
    for page_no, page in enumerate(reader.pages, start=1):
        for raw in (page.extract_text() or "").splitlines():
            text = " ".join(raw.split())
            if text and not PAGE_NUMBER_RE.match(text):
                lines.append((page_no, text))
    return lines


def truncate(text, limit=MAX_EXPLANATION):
    """Cut to at most `limit` chars, preferring the last sentence boundary."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    ends = [m.start() + 1 for m in SENTENCE_END_RE.finditer(cut)]
    return cut[:ends[-1]] if ends else cut.rstrip()


def split_chapters(lines):
    """Group lines under chapter headings. Returns raw chapters with body lines."""
    chapters, current, i = [], None, 0
    while i < len(lines):
        page_no, text = lines[i]
        m = HEADING_RE.match(text) if len(text) < 120 else None
        i += 1
        if m:
            title = m.group(3).strip(" -:.")
            if not title and i < len(lines):
                title = lines[i][1]
                i += 1
            current = {"chapter_number": m.group(2), "chapter_title": title,
                       "page_start": page_no, "page_end": page_no, "body": []}
            chapters.append(current)
        elif current is not None:
            if not EXERCISE_RE.match(text):
                current["body"].append(text)
            current["page_end"] = page_no
    return chapters


def build_chapters(pdf):
    """Return chapter dicts (without class/subject/medium/source) for one PDF."""
    reader = PdfReader(str(pdf))
    lines = clean_lines(reader)
    if not lines:
        return []
    raw_chapters = split_chapters(lines)
    if not raw_chapters:
        # No headings at all: whole PDF becomes chapter 1.
        title = " ".join(pdf.stem.replace("_", " ").replace("-", " ").split())
        body = " ".join(text for _, text in lines)
        return [{"chapter_number": "1", "chapter_title": title, "page_start": 1,
                 "page_end": len(reader.pages), "explanation": truncate(body)}]
    records = []
    for ch in raw_chapters:
        body = " ".join(ch["body"])
        if len(body) < MIN_BODY_CHARS:
            continue  # table-of-contents entries and empty headings
        records.append({"chapter_number": ch["chapter_number"], "chapter_title": ch["chapter_title"],
                        "page_start": ch["page_start"], "page_end": ch["page_end"],
                        "explanation": truncate(body)})
    return records


def main():
    groups, skipped = {}, []
    if not RAW_DIR.exists():
        print(f"Raw folder not found: {RAW_DIR}")
        return
    for pdf in sorted(RAW_DIR.rglob("*.pdf")):
        rel = pdf.relative_to(RAW_DIR).as_posix()
        try:
            class_num, medium = class_and_medium(pdf)
            if class_num is None:
                print(f"Skipping {rel}: no 'class N' folder in path")
                continue
            subject = subject_from_name(pdf.name)
            # Errata files are included like any other PDF; they only drop out when they yield no text.
            chapters = build_chapters(pdf)
            if not chapters:
                skipped.append(rel)
                continue
            key = (class_num, subject, medium)
            for ch in chapters:
                groups.setdefault(key, []).append(
                    {"class": class_num, "subject": subject, "medium": medium, "source_pdf": rel, **ch})
        except Exception as exc:
            print(f"ERROR {rel}: {exc}")

    for (class_num, subject, medium), records in sorted(groups.items()):
        slug = subject.lower().replace(" ", "_")
        out_path = TOPICS_DIR / f"class{class_num}" / f"{slug}_{medium}.json"
        os.makedirs(out_path.parent, exist_ok=True)
        out_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{out_path}: {len(records)} chapters")

    print(f"Skipped (no text): {len(skipped)}")
    for rel in skipped:
        print(f"  - {rel}")


if __name__ == "__main__":
    main()
