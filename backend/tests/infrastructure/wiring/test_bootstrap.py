import asyncio
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from app.shared.config import Settings


pytestmark = pytest.mark.unit


def test_startup_calls_configure_logging_and_logs(
    settings_factory: Callable[..., Settings], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Startup should configure logging and emit startup messages."""
    settings = settings_factory()

    recorded: dict[str, object] = {}

    # Replace the real configure_logging in the bootstrap module so we can
    # assert it was called with the configured values from settings.
    monkeypatch.setattr(
        "app.infrastructure.wiring.bootstrap.configure_logging",
        lambda level, mode: recorded.update({"level": level, "mode": mode}),
    )

    fake_logger = SimpleNamespace(info=Mock(), debug=Mock())
    monkeypatch.setattr("structlog.get_logger", lambda name=None: fake_logger)

    from app.infrastructure.wiring.bootstrap import startup

    asyncio.run(startup(settings))

    assert recorded.get("level") is settings.logging.level
    assert recorded.get("mode") is settings.logging.mode

    fake_logger.info.assert_called_once_with("application.startup")

    # debug should have been called with the settings payload
    fake_logger.debug.assert_called_once()
    args, kwargs = fake_logger.debug.call_args
    assert args[0] == "application.startup.settings"
    assert "settings" in kwargs
    assert kwargs["settings"] == settings.model_dump(mode="json")


def test_shutdown_logs_application_shutdown(
    settings_factory: Callable[..., Settings], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Shutdown should emit a shutdown message on the bootstrap logger."""
    settings = settings_factory()

    fake_logger = SimpleNamespace(info=Mock(), debug=Mock())
    monkeypatch.setattr("structlog.get_logger", lambda name=None: fake_logger)

    from app.infrastructure.wiring.bootstrap import shutdown

    asyncio.run(shutdown(settings))

    fake_logger.info.assert_called_once_with("application.shutdown")
