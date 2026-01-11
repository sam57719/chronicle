"""System API router module."""

from fastapi import APIRouter

from .schemas import HealthCheckResponse, HealthStatus

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check() -> HealthCheckResponse:
    """Get health of the system."""
    return HealthCheckResponse(status=HealthStatus.OK)
