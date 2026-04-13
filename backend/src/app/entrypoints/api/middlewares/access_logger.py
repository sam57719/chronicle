import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def access_log_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware function to log HTTP request and response details."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    client = request.client.host if request.client else "-"
    print(
        f"{client} "
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{duration_ms:.3f}ms"
    )
    return response
