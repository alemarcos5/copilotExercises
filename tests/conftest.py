import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for each test"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset the in-memory database before each test.
    This ensures test isolation and removes changes from other tests.
    """
    # Store the original state
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "School basketball team with competitive games and training",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and play matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["sophia@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM topics",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu"]
        }
    }
    
    # Clear and restore the activities dictionary
    activities.clear()
    activities.update(original_state)
    
    yield
    
    # Cleanup after test - restore original state
    activities.clear()
    activities.update(original_state)


@pytest.fixture(autouse=True)
def auto_reset(reset_activities):
    """Automatically reset state before each test"""
    pass
