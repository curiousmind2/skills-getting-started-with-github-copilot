from src.app import activities


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(endpoint, params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert len(activities[activity_name]["participants"]) == initial_count + 1
    assert new_email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(endpoint, params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"
    assert len(activities[activity_name]["participants"]) == initial_count


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
