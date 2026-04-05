from http import HTTPStatus

from fastapi import APIRouter

from .schemas import HealthCheckResponse

router: APIRouter = APIRouter(tags=["System"])


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
