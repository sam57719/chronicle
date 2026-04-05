from http import HTTPStatus

from fastapi import APIRouter

from .schemas import HealthCheckResponse

router: APIRouter = APIRouter(tags=["System"])


@router.get(
    "/health",
    summary="Health Check",
    description="Is the system online?",
    status_code=HTTPStatus.OK,
)
async def health_check() -> HealthCheckResponse:
    """Get health of the system."""
    return HealthCheckResponse(status="ok")
