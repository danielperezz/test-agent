# Tests Directory

This directory contains unit tests for the `simple_agent` FastAPI application.

## Running Tests

To run all tests:
```bash
pytest tests/
```

To run with verbose output:
```bash
pytest tests/ -v
```

To run with coverage:
```bash
pytest tests/ --cov=simple_agent --cov-report=html
```

To run a specific test file:
```bash
pytest tests/test_main.py
```

To run a specific test:
```bash
pytest tests/test_main.py::TestHealthCheck::test_health_check_success
```

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
  - Environment variable setup
  - Test client fixture
  - API key fixtures

- `test_main.py` - Main endpoint tests
  - Health check endpoint tests
  - Root endpoint tests
  - Echo endpoint tests (valid/invalid API keys, uppercase, edge cases)
  - Environment variable handling tests
  - Input validation tests

- `test_startup.py` - Application startup and configuration tests
  - API key validation tests
  - Default configuration tests
  - Environment variable tests

## Test Coverage

The test suite covers:
- ✅ All API endpoints (`/`, `/health`, `/echo`)
- ✅ API key authentication
- ✅ Message processing (uppercase/normal)
- ✅ Environment variable configuration
- ✅ Input validation and error handling
- ✅ Edge cases (empty messages, special characters, etc.)

## Requirements

The following packages are required to run tests:
- `pytest==8.0.0` - Testing framework
- `httpx==0.27.0` - HTTP client for testing FastAPI applications

These are included in `requirements.txt`.
