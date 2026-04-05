from typing import Literal

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: Literal["ok"]
