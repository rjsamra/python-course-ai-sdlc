from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel

router = APIRouter(
    prefix="/flights",
    tags=["flights"],
)

class FlightNameUpdate(BaseModel):
    flight_new_name: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def read_flights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    flights = db.query(models.Flight).offset(skip).limit(limit).all()
    return flights

@router.get("/{flight_id}")
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(models.Flight).filter(models.Flight.flight_id == flight_id).first()
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

@router.put("/{flight_id}/name")
def update_flight_name(flight_id: int, flight_update: FlightNameUpdate, db: Session = Depends(get_db)):
    """Update the flight number of a specific flight."""
    flight = db.query(models.Flight).filter(models.Flight.flight_id == flight_id).first()
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    flight.flight_no = flight_update.flight_new_name
    db.commit()
    db.refresh(flight)
    return flight
