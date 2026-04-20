import time
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def access_log_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware to log basic HTTP request/response details via structlog.

    Logs only method/path/client/query/status/duration; no bodies or headers.
    """
    logger = structlog.get_logger("access")

    # noinspection PyUnresolvedReferences
    client = request.client.host if request.client else None

    request_data = {
        "path": request.url.path,
        "method": request.method,
        "client": client,
    }
    if request.query_params:
        request_data["query"] = str(request.query_params)

    await logger.ainfo("http.request", **request_data)

    start = time.perf_counter()
    response: Response
    try:
        response = await call_next(request)
    except Exception as exc:
        duration_ms = (time.perf_counter() - start) * 1000
        await logger.aexception(
            "http.response.exception",
            exc_info=exc,
            stack_info=True,
            path=request.url.path,
            method=request.method,
            client=client,
            duration_ms=round(duration_ms, 3),
        )
        raise
    else:
        duration_ms = (time.perf_counter() - start) * 1000
        response_data = {
            "duration_ms": round(duration_ms, 3),
            "status_code": response.status_code,
        }

        await logger.ainfo("http.response", **response_data)
        return response
