"""Contract tests for Curriculum API service."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_classes():
    response = client.get("/v1/classes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10
    # Verify Class 1 to Class 10
    numbers = [c["number"] for c in data]
    assert numbers == list(range(1, 11))


def test_get_subjects_for_class_10():
    response = client.get("/v1/classes/10/subjects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    names = [s["name"] for s in data]
    assert any("Mathematics" in n for n in names)
    assert any("Biology" in n for n in names)
    assert any("Telugu" in n for n in names)


def test_get_subjects_by_medium():
    # Test English Medium
    em_res = client.get("/v1/classes/10/subjects?medium=EM")
    assert em_res.status_code == 200
    em_data = em_res.json()
    assert len(em_data) == 5
    em_names = [s["name"] for s in em_data]
    assert "Mathematics" in em_names
    assert "Biological Science" in em_names
    assert "Physical Science" in em_names
    assert "Social Studies" in em_names
    assert "English Reader" in em_names
    for s in em_data:
        assert s["medium"] == "EM"

    # Test Telugu Medium
    tm_res = client.get("/v1/classes/10/subjects?medium=TM")
    assert tm_res.status_code == 200
    tm_data = tm_res.json()
    assert len(tm_data) == 6
    for s in tm_data:
        assert s["medium"] == "TM"


def test_get_chapters_for_all_subjects():
    for sub in ["math_10", "bio_10", "phy_10", "soc_10", "eng_10", "tel_10"]:
        res = client.get(f"/v1/classes/10/subjects/{sub}/chapters")
        assert res.status_code == 200
        chaps = res.json()
        assert len(chaps) > 0
        assert len(chaps[0]["topics"]) > 0


def test_get_chapters_for_biology():
    response = client.get("/v1/classes/10/subjects/bio_10/chapters")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    titles = [ch["title"] for ch in data]
    assert any("Nutrition" in t or "పోషణ" in t for t in titles)
    assert any("Respiration" in t or "శ్వాసక్రియ" in t for t in titles)

    # Check topics within chapter
    ch1 = next(ch for ch in data if "Nutrition" in ch["title"] or "పోషణ" in ch["title"])
    assert len(ch1["topics"]) > 0


def test_get_latest_updates():
    response = client.get("/v1/curriculum/latest-updates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]
    assert "date" in data[0]


def test_get_chapter_package():
    response = client.get("/v1/curriculum/packages/bio_10/bio_10_ch01")
    assert response.status_code == 200
    data = response.json()
    assert data["package_version"] == "1.0.0"
    assert data["subject_id"] == "bio_10"
    assert data["chapter_id"] == "bio_10_ch01"
    assert len(data["topics"]) > 0
    assert len(data["workbook_activities"]) > 0
    assert len(data["educational_games"]) > 0
    assert len(data["cached_video_metadata"]) > 0
    assert len(data["vector_db_slice"]) > 0
    assert "checksum" in data
    # Video metadata must indicate streaming only
    assert data["cached_video_metadata"][0]["online_streaming_only"] is True
