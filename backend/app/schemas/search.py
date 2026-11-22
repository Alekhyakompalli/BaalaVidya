"""Search Pydantic schemas."""


from pydantic import BaseModel


class SearchResultItem(BaseModel):
    chunk_id: str
    title: str
    subject: str
    chapter: str
    class_name: str
    language: str
    snippet: str
    score: float
    source_page: int | None = None


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[SearchResultItem]
