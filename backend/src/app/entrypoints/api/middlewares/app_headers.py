from typing import TYPE_CHECKING

from app.shared.config import Settings, get_settings

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def apply_app_response_headers(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware to apply application headers to the response."""
    settings: Settings = get_settings()

    response: Response = await call_next(request)
    response.headers["X-Application-Name"] = settings.app.display_name
    response.headers["X-Application-Version"] = settings.app.version
    return response
