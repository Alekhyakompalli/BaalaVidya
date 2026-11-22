"""Search service supporting keyword and concept matching over syllabus and chunks across all classes."""

from app.schemas.search import SearchResponse, SearchResultItem
from app.services.curriculum_data import CURRICULUM_DATA
from app.services.retriever import retrieve


def search_syllabus_and_chunks(
    query: str,
    class_name: str | None = None,
    subject: str | None = None,
    limit: int = 10,
) -> SearchResponse:
    """
    Search over curriculum topics and Qdrant chunk index across all classes or a targeted class.
    """
    results: list[SearchResultItem] = []
    q_lower = query.lower().strip()

    # Determine classes to search
    target_classes = ["6", "7", "8", "9", "10"]
    if class_name and class_name.lower() != "all" and class_name in CURRICULUM_DATA:
        target_classes = [class_name]

    # 1. Metadata / Concept matching on full curriculum structure across classes
    for cls_id in target_classes:
        cls_data = CURRICULUM_DATA.get(cls_id, {})
        for medium in ["EM", "TM"]:
            for s in cls_data.get(medium, []):
                s_name = s.get("name", "")
                s_telugu = s.get("teluguName", s_name)
                display_s_name = s_telugu if medium == "TM" else s_name

                if subject:
                    subj_filter = subject.lower()
                    if subj_filter not in s_name.lower() and subj_filter not in s_telugu.lower() and subj_filter not in s.get("id", "").lower():
                        continue

                for ch in s.get("chapters", []):
                    ch_title = ch["title"]
                    ch_lower = ch_title.lower()
                    ch_num = ch.get("num", 1)

                    # Chapter title match
                    if q_lower in ch_lower or any(w in ch_lower for w in q_lower.split() if len(w) > 3):
                        results.append(
                            SearchResultItem(
                                chunk_id=f"cls{cls_id}_{s.get('id', 's')}_ch{ch_num}_meta",
                                title=f"Class {cls_id} {display_s_name}: {ch_title}",
                                subject=display_s_name,
                                chapter=ch_title,
                                class_name=cls_id,
                                language="te" if medium == "TM" else "en",
                                snippet=f"Class {cls_id} Syllabus: Chapter {ch_num} - {ch_title} in {display_s_name}.",
                                score=0.99,
                            )
                        )

                    # Topic matches
                    for t in ch.get("topics", []):
                        t_lower = t.lower()
                        if q_lower in t_lower or any(w in t_lower for w in q_lower.split() if len(w) > 3):
                            results.append(
                                SearchResultItem(
                                    chunk_id=f"cls{cls_id}_{s.get('id', 's')}_ch{ch_num}_top_{hash(t)%10000}",
                                    title=f"Class {cls_id} {display_s_name} - {ch_title} -> {t}",
                                    subject=display_s_name,
                                    chapter=ch_title,
                                    class_name=cls_id,
                                    language="te" if medium == "TM" else "en",
                                    snippet=f"Curriculum Topic: {t} (Class {cls_id} {display_s_name}, Chapter {ch_num}).",
                                    score=0.95,
                                )
                            )

    # 2. Semantic retrieval from Qdrant chunks
    try:
        retrieval_class = None if (class_name is None or class_name.lower() == "all") else class_name
        hits = retrieve(query, class_name=retrieval_class, subject=subject, top_k=limit, score_threshold=0.55)
        for h in hits:
            results.append(
                SearchResultItem(
                    chunk_id=h["chunk_id"],
                    title=f"Class {h.get('class_name', '10')} {h['subject']} - {h['chapter']}",
                    subject=h["subject"],
                    chapter=h["chapter"],
                    class_name=str(h.get("class_name", "10")),
                    language=h.get("language", "en"),
                    snippet=h.get("text", "")[:200],
                    score=round(h["score"], 3),
                    source_page=h.get("source_page"),
                )
            )
    except Exception as e:  # noqa: BLE001
        print(f"[Search Retrieval Error] {e}")

    # Deduplicate results by chunk_id
    seen_ids = set()
    deduped = []
    for r in results:
        if r.chunk_id not in seen_ids:
            seen_ids.add(r.chunk_id)
            deduped.append(r)

    # Sort by score descending
    deduped.sort(key=lambda x: x.score, reverse=True)
    final_results = deduped[:limit]

    return SearchResponse(
        query=query,
        total_results=len(final_results),
        results=final_results,
    )
