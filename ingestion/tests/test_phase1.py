"""Phase 1 verification tests: Curriculum Ingestion Pipeline.

Verifies:
1. Chunk schema completeness (all fields present, correct types)
2. Chunk-ID determinism (running twice produces identical chunk IDs)
3. Qdrant local vector store integrity (points indexed, payload preserved)
4. Bilingual retrieval accuracy on curated test set (Recall@5 >= 0.80 for both English & Telugu)
5. Telugu OCR quality and character integrity
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path so 'ingestion' package can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import json
import pytest
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent.parent
CHUNKS_PATH = HERE / "data" / "chunks" / "class10_pilot.jsonl"
QDRANT_PATH = HERE / "data" / "qdrant_local"
OCR_CACHE = HERE / "data" / "ocr_cache"

MANDATORY_FIELDS = {
    "chunk_id": str,
    "class": str,
    "subject": str,
    "medium": str,
    "language": str,
    "chapter": str,
    "topic": str,
    "source_file": str,
    "source_sha256": str,
    "source_page": int,
    "chunk_index": int,
    "text": str,
}


def load_chunks():
    assert CHUNKS_PATH.exists(), f"Chunks file not found at {CHUNKS_PATH}"
    records = []
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def test_chunk_schema_complete():
    """Verify each chunk contains all required metadata fields with correct types."""
    chunks = load_chunks()
    assert len(chunks) > 100, f"Expected > 100 pilot chunks, found {len(chunks)}"

    en_count = 0
    te_count = 0
    for idx, c in enumerate(chunks):
        for field, expected_type in MANDATORY_FIELDS.items():
            assert field in c, f"Chunk {idx} ({c.get('chunk_id')}) missing field: {field}"
            assert isinstance(c[field], expected_type), f"Chunk {idx} field {field} expected {expected_type}, got {type(c[field])}"

        assert c["class"] == "10", f"Chunk {idx} class must be '10', got {c['class']}"
        assert c["language"] in ["en", "te"], f"Chunk {idx} language must be 'en' or 'te'"
        assert len(c["text"]) >= 50, f"Chunk {idx} text too short ({len(c['text'])} chars)"
        assert len(c["chunk_id"]) == 36, f"Chunk {idx} ID should be a 36-char UUID"

        if c["language"] == "en":
            en_count += 1
        elif c["language"] == "te":
            te_count += 1

    assert en_count > 0, "No English chunks found"
    assert te_count > 0, "No Telugu chunks found"
    print(f"\n[Schema Check Passed] Total chunks: {len(chunks)} (English: {en_count}, Telugu: {te_count})")


def test_chunk_id_determinism():
    """Verify that re-extracting and chunking produces 100% identical chunk IDs."""
    from ingestion.pipeline import process_entry, PILOT_CONFIG
    # Run process_entry for Biology TM
    bio_tm_entry = next(e for e in PILOT_CONFIG if e["file"] == "X Biology TM Inner 2026-27.pdf")
    records_1, _, _ = process_entry(bio_tm_entry)
    records_2, _, _ = process_entry(bio_tm_entry)

    ids_1 = [r["chunk_id"] for r in records_1]
    ids_2 = [r["chunk_id"] for r in records_2]

    assert len(ids_1) > 0, "No chunks generated in run 1"
    assert ids_1 == ids_2, "Chunk IDs differ between identical pipeline runs!"
    print(f"\n[Determinism Check Passed] {len(ids_1)} chunks produced identical IDs across runs.")


def test_qdrant_pilot_index():
    """Verify Qdrant local collection exists, has points, and matches expected configuration."""
    assert QDRANT_PATH.exists(), f"Qdrant directory {QDRANT_PATH} does not exist"
    client = QdrantClient(path=str(QDRANT_PATH))

    # Verify official pilot_chunks collection exists
    assert client.collection_exists("pilot_chunks"), "Collection 'pilot_chunks' does not exist in Qdrant!"
    info = client.get_collection("pilot_chunks")
    assert info.points_count > 0, f"Collection 'pilot_chunks' is empty ({info.points_count} points)"
    assert info.config.params.vectors.size in [768, 1024], f"Unexpected vector dimension: {info.config.params.vectors.size}"

    # Sample a point and verify payload fields
    sample_points, _ = client.scroll(collection_name="pilot_chunks", limit=1, with_payload=True)
    assert len(sample_points) == 1
    payload = sample_points[0].payload
    for field in ["chunk_id", "class", "subject", "chapter", "language", "source_page"]:
        assert field in payload, f"Qdrant payload missing {field}"

    print(f"\n[Qdrant Check Passed] Collection 'pilot_chunks': {info.points_count} points, dim={info.config.params.vectors.size}")


def test_bilingual_retrieval_recall():
    """Verify that retrieval recall on curated syllabus questions meets or exceeds 0.80."""
    from ingestion.embed_eval import CURATED_QUERIES, MODELS
    client = QdrantClient(path=str(QDRANT_PATH))

    # Determine which model is used for pilot_chunks by checking dimension
    info = client.get_collection("pilot_chunks")
    dim = info.config.params.vectors.size
    model_key = "e5_base" if dim == 768 else "bge_m3"
    cfg = MODELS[model_key]

    model = SentenceTransformer(cfg["hf"], local_files_only=True)
    top_k = 5

    en_queries = [q for q in CURATED_QUERIES if q["language"] == "en"]
    te_queries = [q for q in CURATED_QUERIES if q["language"] == "te"]

    def evaluate_set(queries):
        hits_count = 0
        for q in queries:
            qvec = model.encode(cfg["query_prefix"] + q["query"], normalize_embeddings=True).tolist()
            hits = client.query_points(collection_name="pilot_chunks", query=qvec, limit=top_k).points
            matched = any(
                h.payload.get("chapter") == q["expected_chapter"] and h.payload.get("subject") == q["subject"]
                for h in hits
            )
            if matched:
                hits_count += 1
        return hits_count / len(queries) if queries else 0.0

    en_recall = evaluate_set(en_queries)
    te_recall = evaluate_set(te_queries)

    print(f"\n[Retrieval Recall] English Recall@5 = {en_recall:.1%}, Telugu Recall@5 = {te_recall:.1%}")
    assert en_recall >= 0.80, f"English Recall@5 ({en_recall:.1%}) below 80% threshold!"
    assert te_recall >= 0.80, f"Telugu Recall@5 ({te_recall:.1%}) below 80% threshold!"


def test_telugu_ocr_quality():
    """Verify Telugu OCR files have valid character density, length, and non-corrupted text."""
    txt_files = [f for f in OCR_CACHE.glob("*.txt") if "telugu" in f.name.lower() or "biology_tm" in f.name.lower()]
    assert len(txt_files) >= 50, f"Expected >= 50 cached OCR files, found {len(txt_files)}"

    for f in txt_files:
        text = f.read_text(encoding="utf-8")
        assert len(text) > 100, f"File {f.name} unexpectedly short ({len(text)} chars)"
        tel_count = sum(1 for c in text if 0x0C00 <= ord(c) <= 0x0C7F)
        # Should be predominantly Telugu
        ratio = tel_count / max(len(text.replace(" ", "").replace("\n", "")), 1)
        assert ratio > 0.40, f"File {f.name} low Telugu character ratio ({ratio:.1%})"

    print(f"\n[OCR Quality Check Passed] Verified {len(txt_files)} Telugu OCR pages (all > 40% Telugu Unicode density).")
