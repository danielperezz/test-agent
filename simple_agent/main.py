"""
Simple Example Agent - FastAPI Application

This is a minimal example agent demonstrating:
- Environment variable consumption (SERVICE_NAME, LOG_LEVEL)
- Secret consumption (API_KEY, DATABASE_PASSWORD)
- Health check endpoint
- Echo service endpoint
"""

import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

# Read configuration from environment variables
SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
API_KEY = os.getenv("API_KEY")  # Secret - required
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")  # Secret - optional

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=f"[{SERVICE_NAME}] %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Simple Example Agent",
    description="A minimal marketplace agent demonstrating env vars and secrets",
    version="0.1.0"
)

# Request/Response models
class EchoRequest(BaseModel):
    """Request model for echo endpoint."""
    message: str
    uppercase: bool = False


class EchoResponse(BaseModel):
    """Response model for echo endpoint."""
    service_name: str
    original_message: str
    processed_message: str
    has_database: bool


@app.on_event("startup")
async def startup_event():
    """Log configuration on startup."""
    logger.info("Starting Simple Example Agent")
    logger.info(f"Service Name: {SERVICE_NAME}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info(f"API Key Configured: {bool(API_KEY)}")
    logger.info(f"Database Password Configured: {bool(DATABASE_PASSWORD)}")

    # Validate required secrets
    if not API_KEY:
        logger.error("API_KEY is required but not set!")
        raise RuntimeError("Missing required secret: API_KEY")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": "0.1.0"
    }


@app.post("/echo")
async def echo(
    request: EchoRequest,
    x_api_key: Optional[str] = Header(None)
) -> EchoResponse:
    """
    Echo endpoint - processes and returns the message.

    Demonstrates:
    - API key validation (using secret)
    - Message processing
    - Optional database availability check

    Args:
        request: Echo request with message
        x_api_key: API key from header (must match API_KEY secret)

    Returns:
        EchoResponse: Processed message response

    Raises:
        HTTPException: If API key is invalid
    """
    # Validate API key
    if x_api_key != API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Process message
    processed = request.message.upper() if request.uppercase else request.message
    processed = f"[{SERVICE_NAME}] {processed}"

    logger.info(f"Processing message", extra={"message_length": len(request.message)})

    return EchoResponse(
        service_name=SERVICE_NAME,
        original_message=request.message,
        processed_message=processed,
        has_database=bool(DATABASE_PASSWORD)
    )


@app.get("/")
async def root():
    """
    Root endpoint - returns service information.

    Returns:
        dict: Service information
    """
    return {
        "service": SERVICE_NAME,
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "echo": "/echo (POST)",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
