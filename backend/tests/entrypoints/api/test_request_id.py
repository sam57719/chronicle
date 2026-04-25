import asyncio
from types import SimpleNamespace
from typing import Any, cast

import pytest

pytestmark = pytest.mark.unit


def _make_call_next() -> Any:
    # noinspection PyUnusedLocal
    async def _call_next(request: Any) -> object:
        resp = SimpleNamespace()
        resp.headers = {}
        resp.status_code = 200
        return resp

    return _call_next


# noinspection DuplicatedCode
def test_request_id_middleware_binds_and_attaches_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, object] = {}

    def fake_clear() -> None:
        recorded["cleared"] = True

    def fake_bind(**kwargs: Any) -> None:
        recorded["bound"] = kwargs

    monkeypatch.setattr("structlog.contextvars.clear_contextvars", fake_clear)
    monkeypatch.setattr("structlog.contextvars.bind_contextvars", fake_bind)

    from app.entrypoints.api.middlewares.request_id import request_id_middleware

    request = SimpleNamespace()
    request.headers = {"X-Request-ID": "req-xyz"}

    result = asyncio.run(
        cast(Any, request_id_middleware)(cast(Any, request), _make_call_next())
    )

    assert recorded.get("cleared") is True
    assert recorded.get("bound") == {"request_id": "req-xyz"}
    assert result.headers["X-Request-ID"] == "req-xyz"


# noinspection DuplicatedCode
def test_request_id_middleware_generates_uuid_when_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, object] = {}

    def fake_clear() -> None:
        recorded["cleared"] = True

    def fake_bind(**kwargs: Any) -> None:
        recorded["bound"] = kwargs

    monkeypatch.setattr("structlog.contextvars.clear_contextvars", fake_clear)
    monkeypatch.setattr("structlog.contextvars.bind_contextvars", fake_bind)

    from app.entrypoints.api.middlewares.request_id import request_id_middleware

    request = SimpleNamespace()
    request.headers = {}

    result = asyncio.run(
        cast(Any, request_id_middleware)(cast(Any, request), _make_call_next())
    )

    assert recorded.get("cleared") is True
    bound = recorded.get("bound")
    assert isinstance(bound, dict) and "request_id" in bound
    # validate UUID format
    import uuid

    uuid.UUID(bound["request_id"])  # will raise if invalid
    assert result.headers["X-Request-ID"] == bound["request_id"]
