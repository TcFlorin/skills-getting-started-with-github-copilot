import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    original_participants = activities[activity_name]["participants"][:]
    participant_to_remove = original_participants[0]

    try:
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{participant_to_remove}")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {participant_to_remove} from {activity_name}"
        assert participant_to_remove not in activities[activity_name]["participants"]
    finally:
        # Restore state for the next test
        activities[activity_name]["participants"] = original_participants


def test_unregister_unknown_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    unknown_participant = "unknown@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{unknown_participant}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
