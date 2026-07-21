from src.app import activities


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    enrolled_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(endpoint, params={"email": enrolled_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {enrolled_email} from {activity_name}"
    assert len(activities[activity_name]["participants"]) == initial_count - 1
    assert enrolled_email not in activities[activity_name]["participants"]


def test_unregister_rejects_non_enrolled_participant(client):
    # Arrange
    activity_name = "Chess Club"
    not_enrolled_email = "not.enrolled@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(endpoint, params={"email": not_enrolled_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert len(activities[activity_name]["participants"]) == initial_count


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
