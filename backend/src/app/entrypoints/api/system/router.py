from http import HTTPStatus

import structlog
from fastapi import APIRouter, Depends

from app.shared.config import Settings, get_settings

from .schemas import HealthCheckResponse, VersionResponse

router: APIRouter = APIRouter(tags=["System"])

logger = structlog.get_logger(__name__)


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Backend Health Check",
    description="Is the backend online?",
    status_code=HTTPStatus.OK,
    response_description="Backend is online",
)
async def health_check() -> HealthCheckResponse:
    """Get health of the backend."""
    return HealthCheckResponse(status="ok")


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Application version",
    description="Get the packaged application version.",
    status_code=HTTPStatus.OK,
    response_description="Application version",
)
async def version(settings: Settings = Depends(get_settings)) -> VersionResponse:
    """Get the packaged application version."""
    return VersionResponse(version=settings.app.version)
