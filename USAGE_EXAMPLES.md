# Usage Examples

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000/`.

## Example API Requests

### Get Welcome Message
```bash
curl http://localhost:8000/
```

### List Flights
```bash
curl http://localhost:8000/flights/
```

### Get Flight by ID
```bash
curl http://localhost:8000/flights/1
```

### Handle Not Found
```bash
curl http://localhost:8000/flights/999
# Response: { "detail": "Flight not found" }
```

## Running Tests

To run the test suite:
```bash
pytest
```

## Example Test Cases

- **Test root endpoint:**
  - Ensures the root endpoint returns the welcome message.
- **Test listing flights:**
  - Ensures the `/flights/` endpoint returns a list of flights.
- **Test getting a specific flight:**
  - Ensures `/flights/{flight_id}` returns the correct flight or 404 if not found.

---

For more details, see `API_DOCUMENTATION.md`.