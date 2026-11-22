"""Phase 1 stage 1: inventory and text-layer probe for the Class 10 pilot PDFs.

Run from the project root with the ingestion venv:
    ingestion\\.venv\\Scripts\\python.exe ingestion\\extract_probe.py
Writes ingestion/data/SOURCES.md and prints a summary table. Page text is not printed.
"""

import hashlib
import re
from pathlib import Path

import pymupdf  # PyMuPDF

HERE = Path(__file__).resolve().parent
RAW = HERE / "data" / "raw" / "class 10"
OUT = HERE / "data" / "SOURCES.md"

# Byte-identical duplicates (checked by SHA-256): name -> original name.
COPIES = {
    "10 English Reader-2026-27 - Copy.pdf": "10 English Reader-2026-27.pdf",
    "10th Telugu OM Inner Pages 2026-27 - Copy.pdf": "10th Telugu OM Inner Pages 2026-27.pdf",
    "X Mathematics TM 2026-27 - Copy.pdf": "X Mathematics TM 2026-27.pdf",
}

TELUGU = re.compile(r"[\u0C00-\u0C7F]")
LATIN = re.compile(r"[A-Za-z]")
SUBJECTS = [
    ("Mathematics", r"math"),
    ("Physics", r"physics"),
    ("Biology", r"biology"),
    ("Social Studies", r"social"),
    ("Environmental Education", r"environ"),
    ("English", r"english"),
    ("Telugu", r"telugu"),
    ("Sanskrit", r"_san_|san_"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def medium(name: str) -> str:
    n = name.lower()
    if "bilingual" in n or re.search(r"\bbil\b", n):
        return "BIL"
    if re.search(r"\bem\b", n):
        return "EM"
    if re.search(r"\btm\b", n):
        return "TM"
    return "unknown"


def subject(name: str) -> str:
    n = name.lower()
    for label, pattern in SUBJECTS:
        if re.search(pattern, n):
            return label
    return "unknown"


def probe(path: Path) -> dict:
    doc = pymupdf.open(path)
    with_text = without_text = telugu = latin = 0
    for i, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) > 50:
            with_text += 1
        else:
            without_text += 1
        if i < 5:
            telugu += len(TELUGU.findall(text))
            latin += len(LATIN.findall(text))
    pages = doc.page_count
    doc.close()
    return {
        "pages": pages,
        "with_text": with_text,
        "without_text": without_text,
        "telugu_chars_first5": telugu,
        "latin_chars_first5": latin,
    }


def main() -> None:
    all_pdfs = sorted(RAW.glob("*.pdf"))
    unique = [p for p in all_pdfs if p.name not in COPIES]
    rows = []
    failed = []
    print(f"processing {len(unique)} files", flush=True)
    for i, path in enumerate(unique, 1):
        try:
            info = probe(path)
            rows.append(
                {
                    "name": path.name,
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                    "medium": medium(path.name),
                    "subject": subject(path.name),
                    **info,
                }
            )
            print(f"[{i}/{len(unique)}] {path.name} pages={info['pages']} with_text={info['with_text']}", flush=True)
        except Exception as exc:
            print(f"ERROR {path.name}: {type(exc).__name__}: {exc}", flush=True)
            failed.append(path.name)

    copy_checks = []
    for copy_name, original_name in COPIES.items():
        copy_path = RAW / copy_name
        original_path = RAW / original_name
        same = sha256(copy_path) == sha256(original_path)
        copy_checks.append((copy_name, original_name, same))

    lines = [
        "# Phase 1 source inventory: Class 10 pilot",
        "",
        "Source: user-supplied PDFs downloaded from the SCERT eTextBooks site. Rights confirmed by the user.",
        "",
        "| File | Bytes | SHA-256 | Pages | Pages with text | Pages without text | Medium | Subject |",
        "|------|-------|---------|-------|-----------------|--------------------|--------|---------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['name']} | {r['size']} | {r['sha256']} | {r['pages']} | "
            f"{r['with_text']} | {r['without_text']} | {r['medium']} | {r['subject']} |"
        )
    lines += ["", "## Excluded duplicates (SHA-256 checked)", "", "| Copy | Original | Byte-identical |", "|------|----------|----------------|"]
    for copy_name, original_name, same in copy_checks:
        lines.append(f"| {copy_name} | {original_name} | {'yes' if same else 'NO - review'} |")
    if failed:
        lines += ["", "## Failed files", ""] + [f"- {name}" for name in failed]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{'file':60} {'pages':>5} {'txt':>5} {'notxt':>5} {'tel5':>6} {'lat5':>6} {'med':>7} subject")
    for r in rows:
        print(
            f"{r['name'][:60]:60} {r['pages']:>5} {r['with_text']:>5} {r['without_text']:>5} "
            f"{r['telugu_chars_first5']:>6} {r['latin_chars_first5']:>6} {r['medium']:>7} {r['subject']}"
        )
    print(f"\nunique files: {len(rows)}; copies excluded: {len(COPIES)}")
    print(f"wrote {OUT}")
    print(f"failed: {len(failed)}")
    for name in failed:
        print(f"  {name}")


if __name__ == "__main__":
    main()
