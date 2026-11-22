"""OCR pipeline module for Telugu and scanned SCERT textbooks.

Uses PyMuPDF to render pages at 300 DPI and Tesseract OCR with Telugu traineddata.
Caches rendered text locally so that re-runs are instantaneous and deterministic.
"""

import os
import re
import subprocess
from pathlib import Path
import pymupdf

HERE = Path(__file__).resolve().parent
TESSDATA = HERE / "tessdata"
OCR_CACHE = HERE / "data" / "ocr_cache"
TESSERACT_EXE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

TELUGU_RANGE = re.compile(r"[\u0C00-\u0C7F]")
LEGACY_GLYPH_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f\xa0-\xff]")


def is_telugu_unicode(text: str) -> bool:
    """Check if text contains valid Telugu Unicode characters."""
    return bool(TELUGU_RANGE.search(text))


def is_corrupted_font_text(text: str) -> bool:
    """Check if extracted PDF text is using custom 8-bit non-Unicode font encoding."""
    if not text.strip():
        return False
    # If high proportion of control / extended ASCII characters
    matches = len(LEGACY_GLYPH_CHARS.findall(text))
    return (matches / max(len(text), 1)) > 0.15


def get_cache_path(pdf_name: str, page_number: int) -> Path:
    """Return the cache file path for an OCR'd page."""
    stem = Path(pdf_name).stem
    # sanitize stem for filesystem
    safe_stem = re.sub(r"[^\w\-]", "_", stem)
    return OCR_CACHE / f"{safe_stem}_p{page_number:03d}.txt"


def ocr_page(page: pymupdf.Page, pdf_name: str, page_number: int, lang: str = "tel") -> str:
    """Render a PDF page to 300 DPI image and perform OCR using Tesseract."""
    cache_path = get_cache_path(pdf_name, page_number)
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    OCR_CACHE.mkdir(parents=True, exist_ok=True)
    temp_png = OCR_CACHE / f"_tmp_{cache_path.stem}.png"
    temp_base = OCR_CACHE / f"_tmp_{cache_path.stem}"

    # Render at 300 DPI (scale = 300 / 72)
    zoom = 300 / 72
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
    pix.save(str(temp_png))

    cmd = [
        str(TESSERACT_EXE),
        str(temp_png),
        str(temp_base),
        "--tessdata-dir", str(TESSDATA),
        "-l", lang,
        "--psm", "3"
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        out_txt = temp_base.with_suffix(".txt")
        if out_txt.exists():
            text = out_txt.read_text(encoding="utf-8")
            cache_path.write_text(text, encoding="utf-8")
            out_txt.unlink(missing_ok=True)
        else:
            text = ""
    except Exception as e:
        print(f"[OCR Error] {pdf_name} page {page_number}: {e}")
        text = ""
    finally:
        temp_png.unlink(missing_ok=True)

    return text


def extract_page_text(doc: pymupdf.Document, page_number: int, pdf_name: str, is_telugu_pdf: bool = False) -> str:
    """
    Extract text for a 1-based page number.
    If the document is Telugu-medium or uses custom font encoding without Unicode text,
    fall back to OCR.
    """
    page = doc.load_page(page_number - 1)
    raw_text = page.get_text("text")

    # If it's explicitly Telugu-medium or text is missing / corrupted font encoding:
    if is_telugu_pdf:
        # Check if raw_text actually contains genuine Unicode Telugu
        tel_count = len(TELUGU_RANGE.findall(raw_text))
        if tel_count < 20 or is_corrupted_font_text(raw_text):
            return ocr_page(page, pdf_name, page_number, lang="tel")
        return raw_text

    # English / general check
    if is_corrupted_font_text(raw_text):
        return ocr_page(page, pdf_name, page_number, lang="eng")

    return raw_text
