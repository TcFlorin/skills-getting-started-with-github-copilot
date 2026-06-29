import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]

    try:
        response = client.delete(f"/activities/{activity_name}/participants/{original_participants[0]}")

        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {original_participants[0]} from {activity_name}"
        assert original_participants[0] not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_unknown_participant_returns_not_found():
    activity_name = "Chess Club"
    response = client.delete(f"/activities/{activity_name}/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
