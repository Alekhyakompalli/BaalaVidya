"""Contract tests for Search API service."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_concept_photosynthesis():
    response = client.get("/v1/search?q=photosynthesis")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "photosynthesis"
    assert data["total_results"] > 0
    assert len(data["results"]) > 0

    # Ensure topic or chapter related to Photosynthesis / Nutrition is returned
    top = data["results"][0]
    assert "chunk_id" in top
    assert "title" in top
    assert "score" in top


def test_search_mathematics_polynomials():
    response = client.get("/v1/search?q=polynomials&subject=Mathematics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] > 0
    assert any("Polynomial" in r["chapter"] or "Polynomial" in r["title"] for r in data["results"])


def test_search_telugu_query():
    response = client.get("/v1/search?q=కిరణజన్య")
    assert response.status_code == 200
    data = response.json()
    assert data["total_results"] > 0
