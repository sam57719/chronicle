from typing import Literal

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: Literal["ok"]


class VersionResponse(BaseModel):
    """Response schema for the application/package version endpoint."""

    version: str
