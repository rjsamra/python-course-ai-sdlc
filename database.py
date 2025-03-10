import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./flights.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    import models
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing database: {e}")
        if "file is not a database" in str(e) or "no such column" in str(e):
            os.remove("flights.db")
            Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Insert dummy data
    if not db.query(models.Flight).first():
        dummy_flights = [
            models.Flight(
                flight_id=1,
                flight_no="AA123",
                flight_name="{{indigo}}",  # New field
                scheduled_departure=datetime(2023, 10, 1, 8, 0, 0),
                scheduled_arrival=datetime(2023, 10, 1, 12, 0, 0),
                departure_airport="JFK",
                arrival_airport="LAX",
                status="On Time",
                aircraft_code="A320",
                actual_departure=datetime(2023, 10, 1, 8, 5, 0),
                actual_arrival=datetime(2023, 10, 1, 12, 5, 0)
            ),
            models.Flight(
                flight_id=2,
                flight_no="BA456",
                flight_name="{{indigo}}",  # New field
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
