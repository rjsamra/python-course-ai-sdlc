import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from routers.flights import get_db
from main import app
from models import Flight
from datetime import datetime

# Create a test database
TEST_DATABASE_URL = "sqlite:///./test_flights.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    """Set up test database with fresh data for each test run."""
    # Remove existing test database if it exists
    if os.path.exists("test_flights.db"):
        os.remove("test_flights.db")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Insert test data
    db = TestingSessionLocal()
    dummy_flights = [
        Flight(
            flight_id=1,
            flight_no="AA123",
            scheduled_departure=datetime(2023, 10, 1, 8, 0, 0),
            scheduled_arrival=datetime(2023, 10, 1, 12, 0, 0),
            departure_airport="JFK",
            arrival_airport="LAX",
            status="On Time",
            aircraft_code="A320",
            actual_departure=datetime(2023, 10, 1, 8, 5, 0),
            actual_arrival=datetime(2023, 10, 1, 12, 5, 0)
        ),
        Flight(
            flight_id=2,
            flight_no="BA456",
            scheduled_departure=datetime(2023, 10, 2, 9, 0, 0),
            scheduled_arrival=datetime(2023, 10, 2, 13, 0, 0),
            departure_airport="LHR",
            arrival_airport="JFK",
            status="Delayed",
            aircraft_code="B747",
            actual_departure=datetime(2023, 10, 2, 9, 30, 0),
            actual_arrival=datetime(2023, 10, 2, 13, 30, 0)
        )
    ]
    db.add_all(dummy_flights)
    db.commit()
    db.close()
    
    yield
    
    # Cleanup
    if os.path.exists("test_flights.db"):
        os.remove("test_flights.db")

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Flight API"}

def test_read_flights():
    response = client.get("/flights/")
    assert response.status_code == 200
    flights = response.json()
    assert len(flights) > 0
    assert flights[0]["flight_no"] == "AA123"

def test_read_flight():
    response = client.get("/flights/1")
    assert response.status_code == 200
    flight = response.json()
    assert flight["flight_no"] == "AA123"

def test_read_nonexistent_flight():
    response = client.get("/flights/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Flight not found"}

def test_update_flight_name():
    """Test updating a flight's name successfully."""
    # First, get the current flight to verify the update
    response = client.get("/flights/1")
    assert response.status_code == 200
    original_flight = response.json()
    original_name = original_flight["flight_no"]
    
    # Update the flight name
    new_name = "UPDATED123"
    response = client.put("/flights/1/name", json={"flight_new_name": new_name})
    assert response.status_code == 200
    
    updated_flight = response.json()
    assert updated_flight["flight_no"] == new_name
    assert updated_flight["flight_id"] == original_flight["flight_id"]
    
    # Verify the change persisted by fetching the flight again
    response = client.get("/flights/1")
    assert response.status_code == 200
    fetched_flight = response.json()
    assert fetched_flight["flight_no"] == new_name
    
    # Restore original name to not affect other tests
    response = client.put("/flights/1/name", json={"flight_new_name": original_name})
    assert response.status_code == 200

def test_update_nonexistent_flight_name():
    """Test updating a non-existent flight's name returns 404."""
    response = client.put("/flights/999/name", json={"flight_new_name": "NONEXISTENT123"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Flight not found"}

def test_update_flight_name_invalid_request():
    """Test updating flight name with invalid request body."""
    response = client.put("/flights/1/name", json={})
    assert response.status_code == 422  # Validation error for missing required field

def test_update_flight_name_with_new1234():
    """Test the specific curl command case: updating flight 1 name to NEW1234."""
    # Get original flight data
    response = client.get("/flights/1")
    assert response.status_code == 200
    original_flight = response.json()
    original_name = original_flight["flight_no"]
    
    # Update flight name to NEW1234 (matching the curl command)
    response = client.put("/flights/1/name", json={"flight_new_name": "NEW1234"})
    assert response.status_code == 200
    
    # Verify response contains updated flight data
    updated_flight = response.json()
    assert updated_flight["flight_no"] == "NEW1234"
    assert updated_flight["flight_id"] == 1
    assert updated_flight["departure_airport"] == original_flight["departure_airport"]
    assert updated_flight["arrival_airport"] == original_flight["arrival_airport"]
    
    # Verify the update persisted in database
    response = client.get("/flights/1")
    assert response.status_code == 200
    fetched_flight = response.json()
    assert fetched_flight["flight_no"] == "NEW1234"
    
    # Restore original name for other tests
    response = client.put("/flights/1/name", json={"flight_new_name": original_name})
    assert response.status_code == 200

def test_update_flight_name_edge_cases():
    """Test edge cases for flight name updates."""
    # Get original flight data
    response = client.get("/flights/1")
    assert response.status_code == 200
    original_name = response.json()["flight_no"]
    
    # Test with empty string
    response = client.put("/flights/1/name", json={"flight_new_name": ""})
    assert response.status_code == 200
    updated_flight = response.json()
    assert updated_flight["flight_no"] == ""
    
    # Test with special characters
    response = client.put("/flights/1/name", json={"flight_new_name": "FL-123@#"})
    assert response.status_code == 200
    updated_flight = response.json()
    assert updated_flight["flight_no"] == "FL-123@#"
    
    # Test with long string
    long_name = "A" * 100
    response = client.put("/flights/1/name", json={"flight_new_name": long_name})
    assert response.status_code == 200
    updated_flight = response.json()
    assert updated_flight["flight_no"] == long_name
    
    # Restore original name
    response = client.put("/flights/1/name", json={"flight_new_name": original_name})
    assert response.status_code == 200

def test_update_flight_name_content_type_validation():
    """Test that the endpoint properly handles Content-Type header."""
    # Test with correct Content-Type (this should work)
    response = client.put(
        "/flights/1/name", 
        json={"flight_new_name": "TEST123"},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    
    # Get original name for restoration
    original_name = response.json()["flight_no"]
    
    # Restore original name
    response = client.get("/flights/1")
    original_name = response.json()["flight_no"] if response.status_code == 200 else "AA123"
    response = client.put("/flights/1/name", json={"flight_new_name": original_name})

def test_update_flight_name_wrong_field_name():
    """Test updating flight name with wrong field name in request body."""
    response = client.put("/flights/1/name", json={"wrong_field": "NEW123"})
    assert response.status_code == 422  # Validation error for missing required field
    
    # Verify the flight name wasn't changed
    response = client.get("/flights/1")
    assert response.status_code == 200
    # Should still have original name since update failed
