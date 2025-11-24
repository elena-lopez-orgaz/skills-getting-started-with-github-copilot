import urllib.parse
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure at least one known activity exists
    assert "Chess Club" in data
    activity = data["Chess Club"]
    assert "participants" in activity
    assert "max_participants" in activity


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    email = "test.user@example.com"

    # Ensure email is not already present
    resp = client.get("/activities")
    assert resp.status_code == 200
    before = resp.json()
    assert email not in before[activity_name]["participants"]

    # Sign up
    resp = client.post(f"/activities/{urllib.parse.quote(activity_name)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Confirm participant now present
    resp = client.get("/activities")
    assert resp.status_code == 200
    after = resp.json()
    assert email in after[activity_name]["participants"]

    # Unregister
    resp = client.delete(f"/activities/{urllib.parse.quote(activity_name)}/participants", params={"email": email})
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Confirm participant removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    final = resp.json()
    assert email not in final[activity_name]["participants"]
