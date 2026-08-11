from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_activity_catalog():
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


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
