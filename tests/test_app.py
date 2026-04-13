import pytest

def test_get_activities(client):
    """Test GET /activities returns all activities."""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # All activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_successful(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate(client):
    """Test duplicate signup returns error."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Already signed up" in data["detail"]

def test_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_remove_participant_successful(client):
    """Test successful participant removal."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]

def test_remove_participant_not_found(client):
    """Test removing non-existent participant returns 404."""
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]

def test_remove_participant_activity_not_found(client):
    """Test removing participant from non-existent activity returns 404."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

# def test_root_redirect(client):
#     """Test root endpoint redirects to static index."""
#     # Arrange - No special setup needed
#     
#     # Act
#     response = client.get("/")
#     
#     # Assert
#     assert response.status_code == 302  # Found redirect
#     assert response.headers["location"] == "/static/index.html"