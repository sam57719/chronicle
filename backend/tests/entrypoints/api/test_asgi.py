import importlib
import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from app.shared.config import Settings


pytestmark = pytest.mark.unit


def _prepare_asgi_module(
    monkeypatch: pytest.MonkeyPatch,
    settings_factory: Callable[..., Settings],
) -> object:
    """Patch ASGI dependencies and return the wrapped app sentinel for assertions."""
    created_app = object()
    wrapped_app = object()

    def fake_create_app() -> object:
        return created_app

    def fake_wrap_asgi_with_proxy_headers(
        app: object,
        *,
        trusted_hosts: list[str],
    ) -> object:
        assert app is created_app
        assert trusted_hosts == ["127.0.0.1", "10.0.0.0/8"]
        return wrapped_app

    settings = settings_factory(env={"MG_API__TRUSTED_HOSTS": "127.0.0.1,10.0.0.0/8"})

    monkeypatch.setattr("app.entrypoints.api.main.create_app", fake_create_app)
    monkeypatch.setattr("app.shared.config.get_settings", lambda: settings)
    monkeypatch.setattr(
        "granian.utils.proxies.wrap_asgi_with_proxy_headers",
        fake_wrap_asgi_with_proxy_headers,
    )

    return wrapped_app


def test_create_asgi_app_wraps_with_trusted_hosts(
    monkeypatch: pytest.MonkeyPatch,
    settings_factory: Callable[..., Settings],
) -> None:
    wrapped_app = _prepare_asgi_module(monkeypatch, settings_factory)

    from app.entrypoints.api import asgi

    assert asgi.create_asgi_app() is wrapped_app


def test_asgi_module_app_uses_wrapped_create_asgi_app(
    monkeypatch: pytest.MonkeyPatch,
    settings_factory: Callable[..., Settings],
) -> None:
    wrapped_app = _prepare_asgi_module(monkeypatch, settings_factory)

    sys.modules.pop("app.entrypoints.api.asgi", None)
    module = importlib.import_module("app.entrypoints.api.asgi")

    assert module.app is wrapped_app
