import asyncio
from types import SimpleNamespace
from typing import Any, cast

import pytest

pytestmark = pytest.mark.unit


def test_app_response_headers_middleware_applies_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The middleware should attach application name/version headers to the response."""
    from app.shared.config import Settings
    from app.shared.config.app_info import ApplicationInfo

    settings = Settings(app=ApplicationInfo(display_name="TestApp", version="9.9.9"))

    monkeypatch.setattr(
        "app.entrypoints.api.middlewares.app_headers.get_settings", lambda: settings
    )

    # noinspection PyUnusedLocal,PyShadowingNames
    async def _call_next(request: Any) -> object:
        resp = SimpleNamespace()
        resp.headers = {}
        resp.status_code = 200
        return resp

    from app.entrypoints.api.middlewares.app_headers import (
        app_response_headers_middleware,
    )

    request = SimpleNamespace()

    result = asyncio.run(
        cast(Any, app_response_headers_middleware)(
            cast(Any, request), cast(Any, _call_next)
        )
    )

    assert result.headers["Application-Name"] == "TestApp"
    assert result.headers["Application-Version"] == "9.9.9"
