import pytest
from fastapi.testclient import TestClient


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """Test successful signup to an activity"""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "jane.doe@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds participant to activity list"""
        email = "jane.doe@mergington.edu"
        
        # Sign up
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test that signup to non-existent activity returns 404"""
        response = client.post(
            "/activities/Fake%20Club/signup",
            params={"email": "jane.doe@mergington.edu"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_already_signed_up(self, client):
        """Test that signing up twice returns 400"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_different_activities(self, client):
        """Test that same person can sign up for different activities"""
        email = "new.student@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(
            "/activities/Programming%20Class/signup",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Verify both signups worked
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]

    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple students can sign up for same activity"""
        emails = ["student1@mergington.edu", "student2@mergington.edu"]
        
        for email in emails:
            response = client.post(
                "/activities/Gym%20Class/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all signups
        activities = client.get("/activities").json()
        for email in emails:
            assert email in activities["Gym Class"]["participants"]

    def test_signup_increments_participant_count(self, client):
        """Test that participant count increases after signup"""
        activities = client.get("/activities").json()
        initial_count = len(activities["Basketball Team"]["participants"])
        
        # Sign up new student
        client.post(
            "/activities/Basketball%20Team/signup",
            params={"email": "new.player@mergington.edu"}
        )
        
        # Check count increased
        activities = client.get("/activities").json()
        final_count = len(activities["Basketball Team"]["participants"])
        assert final_count == initial_count + 1

    def test_signup_with_special_chars_in_email(self, client):
        """Test signup with email containing special characters"""
        email = "john+sports@mergington.edu"
        
        response = client.post(
            "/activities/Tennis%20Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        activities = client.get("/activities").json()
        assert email in activities["Tennis Club"]["participants"]
