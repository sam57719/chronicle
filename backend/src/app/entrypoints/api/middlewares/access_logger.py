import time
import uuid
from typing import TYPE_CHECKING

import structlog
import structlog.contextvars

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def access_log_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware to log HTTP request/response details via structlog.

    Binds a request id (from header or generated) to each log message.
    """
    structlog.contextvars.clear_contextvars()
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    logger = structlog.get_logger("access")

    start = time.perf_counter()
    response: Response
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.exception("http.request.exception", exc_info=exc, stack_info=True)
        raise
    finally:
        duration_ms = (time.perf_counter() - start) * 1000

        # noinspection PyUnresolvedReferences
        client = request.client.host if request.client else None

        data = {
            "path": request.url.path,
            "method": request.method,
            "client": client,
            "duration_ms": round(duration_ms, 3),
        }
        if request.query_params:
            data["query"] = str(request.query_params)

        if "response" in locals():
            # noinspection PyUnboundLocalVariable
            data["status_code"] = response.status_code

        logger.info("http.request", **data)

    return response
