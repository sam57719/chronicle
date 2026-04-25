import asyncio
from types import SimpleNamespace
from typing import Any, cast

import pytest

pytestmark = pytest.mark.unit


# noinspection DuplicatedCode
def test_access_log_middleware_logs_request_and_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    recorded: dict[str, list[tuple[str, dict[str, object]]]] = {
        "ainfo": [],
        "aexception": [],
    }

    # noinspection PyMethodMayBeStatic
    class FakeLogger:
        async def ainfo(self, event: str, **kwargs: Any) -> None:
            recorded["ainfo"].append((event, kwargs))

        async def aexception(self, event: str, **kwargs: Any) -> None:
            recorded["aexception"].append((event, kwargs))

    monkeypatch.setattr("structlog.get_logger", lambda name=None: FakeLogger())

    # noinspection PyUnusedLocal,PyShadowingNames
    async def _call_next(request: Any) -> object:
        resp = SimpleNamespace()
        resp.status_code = 201
        return resp

    from app.entrypoints.api.middlewares.access_logger import access_log_middleware

    request = SimpleNamespace()
    request.client = SimpleNamespace(host="127.0.0.1")
    request.url = SimpleNamespace(path="/test")
    request.method = "GET"
    request.query_params = {}

    result = asyncio.run(
        cast(Any, access_log_middleware)(cast(Any, request), cast(Any, _call_next))
    )

    assert any(entry[0] == "http.request" for entry in recorded["ainfo"]) is True
    resp_logs = [entry[1] for entry in recorded["ainfo"] if entry[0] == "http.response"]
    assert resp_logs, "http.response not logged"
    assert resp_logs[0]["status_code"] == 201
    assert result.status_code == 201


def test_access_log_middleware_logs_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    # noinspection DuplicatedCode
    recorded: dict[str, list[tuple[str, dict[str, object]]]] = {
        "ainfo": [],
        "aexception": [],
    }

    # noinspection PyMethodMayBeStatic
    class FakeLogger:
        async def ainfo(self, event: str, **kwargs: Any) -> None:
            recorded["ainfo"].append((event, kwargs))

        async def aexception(self, event: str, **kwargs: Any) -> None:
            recorded["aexception"].append((event, kwargs))

    monkeypatch.setattr("structlog.get_logger", lambda name=None: FakeLogger())

    # noinspection PyUnusedLocal,PyShadowingNames
    async def _call_next(request: Any) -> object:
        raise RuntimeError("boom")

    from app.entrypoints.api.middlewares.access_logger import access_log_middleware

    request = SimpleNamespace()
    request.client = SimpleNamespace(host="127.0.0.1")
    request.url = SimpleNamespace(path="/error")
    request.method = "POST"
    request.query_params = {}

    import contextlib

    with contextlib.suppress(RuntimeError):
        asyncio.run(
            cast(Any, access_log_middleware)(cast(Any, request), cast(Any, _call_next))
        )

    # exception log should have been recorded
    assert (
        any(entry[0] == "http.response.exception" for entry in recorded["aexception"])
        is True
    )
