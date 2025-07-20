# Flight Management API Project Context

## Project Overview

This is a FastAPI-based flight management system that provides REST endpoints for managing flight data.

## Current Architecture

- **FastAPI**: Web framework for building the REST API
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (flights.db)
- **Pytest**: Testing framework

## Current Features

- Flight CRUD operations (Create, Read, Update, Delete)
- Database initialization with dummy data
- Basic API endpoints for flights
- Test coverage for main endpoints

## File Structure

- `main.py`: FastAPI application entry point
- `database.py`: Database configuration and initialization
- `models.py`: SQLAlchemy models (Flight model)
- `routers/flights.py`: Flight-related API endpoints
- `tests/test_main.py`: API endpoint tests

## Database Schema

The Flight model includes:

- flight_id (Primary Key)
- flight_no (Flight number)
- scheduled_departure/arrival times
- departure_airport/arrival_airport codes
- status (On Time, Delayed, etc.)
- aircraft_code
- actual_departure/arrival times

## Development Notes

- Database is initialized on startup with dummy data
- Uses dependency injection for database sessions
- Includes proper error handling for 404 cases
- Test client setup for integration testing
