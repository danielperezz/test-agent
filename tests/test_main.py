"""Unit tests for simple_agent.main module."""

import pytest
from fastapi import status


class TestHealthCheck:
    """Tests for the /health endpoint."""

    def test_health_check_success(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "test-service"
        assert data["version"] == "0.1.0"

    def test_health_check_structure(self, client):
        """Test health check response has correct structure."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "service" in data
        assert "version" in data


class TestRootEndpoint:
    """Tests for the / endpoint."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns service information."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service"] == "test-service"
        assert data["version"] == "0.1.0"

    def test_root_endpoint_has_endpoints_info(self, client):
        """Test root endpoint includes endpoint information."""
        response = client.get("/")
        data = response.json()

        assert "endpoints" in data
        assert "health" in data["endpoints"]
        assert "echo" in data["endpoints"]
        assert "docs" in data["endpoints"]


class TestEchoEndpoint:
    """Tests for the /echo endpoint."""

    def test_echo_with_valid_api_key(self, client, valid_api_key):
        """Test echo endpoint with valid API key."""
        response = client.post(
            "/echo",
            json={"message": "Hello World", "uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["service_name"] == "test-service"
        assert data["original_message"] == "Hello World"
        assert data["processed_message"] == "[test-service] Hello World"
        assert data["has_database"] is True

    def test_echo_with_uppercase(self, client, valid_api_key):
        """Test echo endpoint with uppercase transformation."""
        response = client.post(
            "/echo",
            json={"message": "Hello World", "uppercase": True},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["original_message"] == "Hello World"
        assert data["processed_message"] == "[test-service] HELLO WORLD"

    def test_echo_without_uppercase_flag(self, client, valid_api_key):
        """Test echo endpoint without explicit uppercase flag (defaults to False)."""
        response = client.post(
            "/echo",
            json={"message": "test message"},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["processed_message"] == "[test-service] test message"

    def test_echo_with_invalid_api_key(self, client, invalid_api_key):
        """Test echo endpoint with invalid API key."""
        response = client.post(
            "/echo",
            json={"message": "Hello World", "uppercase": False},
            headers={"X-API-Key": invalid_api_key}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid API key" in response.json()["detail"]

    def test_echo_without_api_key(self, client):
        """Test echo endpoint without API key header."""
        response = client.post(
            "/echo",
            json={"message": "Hello World", "uppercase": False}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_echo_with_empty_message(self, client, valid_api_key):
        """Test echo endpoint with empty message."""
        response = client.post(
            "/echo",
            json={"message": "", "uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["original_message"] == ""
        assert data["processed_message"] == "[test-service] "

    def test_echo_with_special_characters(self, client, valid_api_key):
        """Test echo endpoint with special characters."""
        special_message = "Hello! @#$%^&*() 123"
        response = client.post(
            "/echo",
            json={"message": special_message, "uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["original_message"] == special_message
        assert special_message in data["processed_message"]

    def test_echo_response_structure(self, client, valid_api_key):
        """Test echo endpoint response has correct structure."""
        response = client.post(
            "/echo",
            json={"message": "test", "uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        data = response.json()
        assert "service_name" in data
        assert "original_message" in data
        assert "processed_message" in data
        assert "has_database" in data


class TestEnvironmentVariables:
    """Tests for environment variable handling."""

    def test_service_name_from_env(self, client):
        """Test that service name is read from environment."""
        response = client.get("/health")
        data = response.json()
        assert data["service"] == "test-service"

    def test_database_password_indicator(self, client, valid_api_key):
        """Test that database password presence is indicated."""
        response = client.post(
            "/echo",
            json={"message": "test", "uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        data = response.json()
        assert data["has_database"] is True


class TestInputValidation:
    """Tests for input validation."""

    def test_echo_missing_message_field(self, client, valid_api_key):
        """Test echo endpoint with missing message field."""
        response = client.post(
            "/echo",
            json={"uppercase": False},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_echo_invalid_json(self, client, valid_api_key):
        """Test echo endpoint with invalid JSON."""
        response = client.post(
            "/echo",
            data="not valid json",
            headers={
                "X-API-Key": valid_api_key,
                "Content-Type": "application/json"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_echo_wrong_data_type(self, client, valid_api_key):
        """Test echo endpoint with wrong data type for uppercase."""
        response = client.post(
            "/echo",
            json={"message": "test", "uppercase": "not_a_boolean"},
            headers={"X-API-Key": valid_api_key}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
