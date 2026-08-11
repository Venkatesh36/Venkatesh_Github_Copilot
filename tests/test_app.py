from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_the_email():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        activities[activity_name]["participants"].append(email)

        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
