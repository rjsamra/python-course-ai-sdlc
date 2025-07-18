# Flight API Documentation

## Overview
This API provides access to flight information, including listing all flights and retrieving details for a specific flight.

---

## Endpoints

### Root Endpoint
- **GET /**
  - **Description:** Returns a welcome message.
  - **Response Example:**
    ```json
    { "message": "Welcome to the Flight API" }
    ```

### List Flights
- **GET /flights/**
  - **Description:** Retrieve a list of flights with optional pagination.
  - **Query Parameters:**
    - `skip` (int, optional): Number of records to skip (default: 0)
    - `limit` (int, optional): Maximum number of records to return (default: 10)
  - **Response Example:**
    ```json
    [
      {
        "flight_id": 1,
        "flight_name": "{{indigo}}",
        "scheduled_departure": "2023-10-01T08:00:00",
        "scheduled_arrival": "2023-10-01T12:00:00",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "status": "On Time",
        "aircraft_code": "A320",
        "actual_departure": "2023-10-01T08:05:00",
        "actual_arrival": "2023-10-01T12:05:00"
      },
      // ... more flights ...
    ]
    ```

### Get Flight by ID
- **GET /flights/{flight_id}**
  - **Description:** Retrieve details for a specific flight by its ID.
  - **Path Parameters:**
    - `flight_id` (int): The ID of the flight to retrieve.
  - **Response Example (Success):**
    ```json
    {
      "flight_id": 1,
      "flight_name": "{{indigo}}",
      "scheduled_departure": "2023-10-01T08:00:00",
      "scheduled_arrival": "2023-10-01T12:00:00",
      "departure_airport": "JFK",
      "arrival_airport": "LAX",
      "status": "On Time",
      "aircraft_code": "A320",
      "actual_departure": "2023-10-01T08:05:00",
      "actual_arrival": "2023-10-01T12:05:00"
    }
    ```
  - **Response Example (Not Found):**
    ```json
    { "detail": "Flight not found" }
    ```

---

## Data Model: Flight
| Field                | Type      | Description                |
|----------------------|-----------|----------------------------|
| flight_id            | Integer   | Unique flight identifier   |
| flight_name          | String    | Name of the flight         |
| scheduled_departure  | Timestamp | Scheduled departure time   |
| scheduled_arrival    | Timestamp | Scheduled arrival time     |
| departure_airport    | String    | Departure airport code     |
| arrival_airport      | String    | Arrival airport code       |
| status               | String    | Flight status              |
| aircraft_code        | String    | Aircraft code              |
| actual_departure     | Timestamp | Actual departure time      |
| actual_arrival       | Timestamp | Actual arrival time        |

---

## Error Handling
- **404 Not Found:** Returned when a flight with the specified ID does not exist.

---

## Feature Flags
- The `/flights` endpoints are enabled by default. You can control their availability using the `ENABLE_FLIGHTS_API` environment variable.
  - Example: `ENABLE_FLIGHTS_API=false` will disable the flights API routes.