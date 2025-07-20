# Development Workflow

## Running the Application

```bash
# Install dependencies (if using requirements.txt)
pip install -r requirements.txt

# Run the development server
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_main.py
```

## Database Management

- Database is automatically initialized on startup
- SQLite database file: `flights.db`
- Dummy data is inserted if no flights exist
- To reset database: delete `flights.db` and restart application

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Common Development Tasks

1. **Adding new endpoints**: Create in appropriate router file
2. **Adding new models**: Add to `models.py` and update database init
3. **Adding tests**: Create in `tests/` directory following existing patterns
4. **Database changes**: Update models and consider migration strategy

## Code Quality

- Follow PEP 8 style guidelines
- Use type hints where possible
- Include docstrings for complex functions
- Maintain test coverage above 80%
