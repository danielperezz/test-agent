"""Pytest configuration and fixtures for testing simple_agent."""

import os
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_env():
    """Set up environment variables for testing."""
    # Save original environment
    original_env = os.environ.copy()

    # Set test environment variables
    os.environ["SERVICE_NAME"] = "test-service"
    os.environ["LOG_LEVEL"] = "INFO"
    os.environ["API_KEY"] = "test-api-key-12345"
    os.environ["DATABASE_PASSWORD"] = "test-db-password"

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    # Import here to ensure environment variables are set
    from src.main import app
    return TestClient(app)


@pytest.fixture
def valid_api_key():
    """Return the valid API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def invalid_api_key():
    """Return an invalid API key for testing."""
    return "wrong-api-key"
