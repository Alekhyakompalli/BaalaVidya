"""Tests for the warm greeting reply to pure hi/hello messages in Ask Bala Buddy."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.guardrails import is_greeting

client = TestClient(app)


@pytest.mark.parametrize(
    "query",
    ["Hi", "hello", "Hey", "Hii", "Helo", "HELLO!!", "hi 😊", "Hello there!", "Good morning", "  hey  "],
)
def test_pure_greetings_are_detected(query):
    assert is_greeting(query) is True


@pytest.mark.parametrize(
    "query",
    ["What is Photosynthesis?", "Hi, what is photosynthesis?", "", "Who won the cricket match?"],
)
def test_non_greetings_are_not_detected(query):
    assert is_greeting(query) is False


def test_greeting_returns_warm_reply_without_retrieval(monkeypatch):
    calls = []

    def fake_retrieve(**kwargs):
        calls.append(kwargs)
        return []

    monkeypatch.setattr("app.routes.chat.retrieve", fake_retrieve)

    response = client.post("/v1/chat", json={"query": "Hello", "language": "en", "learner_id": None})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert "Bala Buddy" in data["answer"]
    assert "Hello" in data["answer"]
    assert data["retrieved_chunks"] == []
    assert calls == [], "Greeting must not trigger syllabus retrieval"


def test_telugu_greeting_returns_telugu_reply():
    response = client.post("/v1/chat", json={"query": "Hi", "language": "te", "learner_id": None})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert "బాల బడ్డీ" in data["answer"]
