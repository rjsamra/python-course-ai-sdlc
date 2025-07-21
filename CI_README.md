# Flights API CI/CD

[![Flights API CI](https://github.com/rjsamra/python-course-ai-sdlc/actions/workflows/ci.yml/badge.svg)](https://github.com/rjsamra/python-course-ai-sdlc/actions/workflows/ci.yml)

This repository contains a FastAPI-based Flights API with automated CI/CD pipeline using GitHub Actions.

## CI Pipeline Features

The GitHub Actions CI pipeline automatically:

### 🧪 Testing
- Runs tests on Python 3.10, 3.11, and 3.12
- Executes pytest with verbose output
- Generates code coverage reports
- Uploads coverage to Codecov

### 🔍 Code Quality
- Runs Black code formatter checks
- Validates import sorting with isort
- Performs linting with flake8
- Checks for syntax errors and undefined names

### 🔒 Security Scanning
- Scans for known security vulnerabilities with Safety
- Performs static security analysis with Bandit
- Generates security reports

### 🚀 Integration Testing
- Starts the FastAPI application
- Performs live endpoint testing
- Validates API responses

## Workflow Triggers

The CI pipeline runs on:
- Push to `main` branch
- Push to any `feature/**` branch
- Pull requests to `main` branch

## Local Development

To run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from database import init_db; init_db()"

# Run tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

## Pipeline Status

Check the [Actions tab](https://github.com/rjsamra/python-course-ai-sdlc/actions) for the latest pipeline runs and status.
