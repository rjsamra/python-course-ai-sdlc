import pytest
from fastapi.testclient import TestClient
from main import app
from database import init_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()

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
