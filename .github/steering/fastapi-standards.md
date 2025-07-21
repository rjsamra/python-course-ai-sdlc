# FastAPI Development Standards

## Code Organization

- Use dependency injection for database sessions
- Separate routers by domain (flights, users, etc.)
- Keep models in dedicated files
- Use Pydantic models for request/response validation

## Database Standards

- Use SQLAlchemy ORM with declarative base
- Include proper indexing on frequently queried fields
- Use proper foreign key relationships
- Include created_at/updated_at timestamps where appropriate

## API Standards

- Use proper HTTP status codes
- Include comprehensive error handling
- Use consistent response formats
- Add proper API documentation with tags and descriptions
- Include request/response models for validation

## Testing Standards

- Use pytest for testing
- Include unit tests for models and business logic
- Include integration tests for API endpoints
- Use test fixtures for database setup
- Mock external dependencies

## Security Standards

- Validate all input data
- Use proper authentication/authorization
- Sanitize database queries (SQLAlchemy handles this)
- Include rate limiting for production APIs
