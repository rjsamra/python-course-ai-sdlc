from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    flight_id = Column(Integer, primary_key=True, index=True)
    flight_name = Column(String, index=True)  # New field
    scheduled_departure = Column(TIMESTAMP, index=True)
    scheduled_arrival = Column(TIMESTAMP, index=True)
    departure_airport = Column(String, index=True)
    arrival_airport = Column(String, index=True)
    status = Column(String, index=True)
    aircraft_code = Column(String, index=True)
    actual_departure = Column(TIMESTAMP, index=True)
    actual_arrival = Column(TIMESTAMP, index=True)
