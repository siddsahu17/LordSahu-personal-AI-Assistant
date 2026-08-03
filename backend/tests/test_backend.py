import pytest
from fastapi.testclient import TestClient
from app.database import init_db
from app.main import app

# Ensure tables exist
init_db()

def test_health():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"

def test_dashboard():
    with TestClient(app) as client:
        response = client.get("/api/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "briefing" in data
        assert "analytics" in data
        assert "goals" in data

def test_chat_pipeline():
    with TestClient(app) as client:
        # Test chat with weight log intent (V1 LifeEntry)
        payload = {
            "text": "Log my weight as 96.5 kg today",
            "mode": "coach",
            "workspace_id": "fitness"
        }
        response = client.post("/api/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "ADD_LIFE_ENTRY"

        # Test chat with study intent
        study_payload = {
            "text": "I studied SQL joins for 2 hours",
            "mode": "focus",
            "workspace_id": "learning"
        }
        study_resp = client.post("/api/chat", json=study_payload)
        assert study_resp.status_code == 200
        study_data = study_resp.json()
        assert study_data["intent"] == "ADD_LIFE_ENTRY"

def test_life_entries_and_chronicle():
    with TestClient(app) as client:
        # Get life entries
        res = client.get("/api/life-entries")
        assert res.status_code == 200
        entries = res.json()
        assert isinstance(entries, list)

        # Get daily chronicle
        chron_res = client.get("/api/daily-chronicle")
        assert chron_res.status_code == 200
        chron = chron_res.json()
        assert "ai_reflection" in chron

def test_goals():
    with TestClient(app) as client:
        client.post("/api/goals", json={"title": "Master Clean Architecture", "workspace_id": "projects", "target_value": 10.0})
        response = client.get("/api/goals")
        assert response.status_code == 200
        goals = response.json()
        assert len(goals) > 0

def test_timeline():
    with TestClient(app) as client:
        response = client.get("/api/timeline")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
