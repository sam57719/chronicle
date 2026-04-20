import uuid
from contextlib import suppress
from typing import TYPE_CHECKING

import structlog
import structlog.contextvars

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def request_id_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware that binds a request id into structlog.contextvars."""
    structlog.contextvars.clear_contextvars()
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    response: Response | None = None
    try:
        response = await call_next(request)
    finally:
        # Attach the request id to the response so clients can correlate logs.
        if response is not None:
            with suppress(Exception):
                response.headers["X-Request-ID"] = request_id

    assert response is not None
    return response
