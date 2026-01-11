"""System API schemas module."""

from enum import StrEnum

from pydantic import BaseModel


class HealthStatus(StrEnum):
    """Health status enumeration for system API."""

    OK = "ok"


class HealthCheckResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: HealthStatus
