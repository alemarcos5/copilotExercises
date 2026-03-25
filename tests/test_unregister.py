import pytest
from fastapi.testclient import TestClient


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes participant from activity"""
        email = "michael@mergington.edu"
        
        # Verify participant exists
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]
        
        # Unregister
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_activity_not_found(self, client):
        """Test that unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Fake%20Club/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_signed_up(self, client):
        """Test that unregistering when not signed up returns 400"""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "nobody@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_decrements_participant_count(self, client):
        """Test that participant count decreases after unregister"""
        email = "daniel@mergington.edu"
        
        activities = client.get("/activities").json()
        initial_count = len(activities["Chess Club"]["participants"])
        
        # Unregister
        client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        
        # Check count decreased
        activities = client.get("/activities").json()
        final_count = len(activities["Chess Club"]["participants"])
        assert final_count == initial_count - 1

    def test_unregister_twice_fails(self, client):
        """Test that unregistering twice returns 400 on second attempt"""
        email = "daniel@mergington.edu"
        
        # First unregister succeeds
        response1 = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second unregister fails
        response2 = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]

    def test_signup_then_unregister(self, client):
        """Test full cycle: signup, then unregister"""
        email = "cycle.test@mergington.edu"
        
        # Sign up
        signup_response = client.post(
            "/activities/Science%20Club/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify signup
        activities = client.get("/activities").json()
        assert email in activities["Science Club"]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            "/activities/Science%20Club/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify unregister
        activities = client.get("/activities").json()
        assert email not in activities["Science Club"]["participants"]

    def test_unregister_doesnt_affect_other_activities(self, client):
        """Test that unregistering from one activity doesn't affect others"""
        email = "emma@mergington.edu"  # In Programming Class
        
        # Verify initial state
        activities = client.get("/activities").json()
        assert email in activities["Programming Class"]["participants"]
        
        # Unregister from Chess Club (not signed up)
        client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Verify still in Programming Class
        activities = client.get("/activities").json()
        assert email in activities["Programming Class"]["participants"]
