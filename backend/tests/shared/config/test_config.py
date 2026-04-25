from typing import TYPE_CHECKING

import pytest

from app.shared.config import Settings

pytestmark = pytest.mark.unit

if TYPE_CHECKING:
    from collections.abc import Callable


def test_settings_defaults(settings_factory: Callable[..., Settings]) -> None:
    settings = settings_factory()

    assert isinstance(settings, Settings)
    assert settings.app.display_name == "Menagerist"
    assert settings.api.access_log_enabled is True
    assert settings.api.trusted_hosts == "*"


def test_settings_applies_api_env_overrides(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(
        env={
            "MG_API__ACCESS_LOG_ENABLED": "false",
            "MG_API__TRUSTED_HOSTS": "127.0.0.1,10.0.0.0/8",
        }
    )

    assert settings.api.access_log_enabled is False
    assert settings.api.trusted_hosts == ["127.0.0.1", "10.0.0.0/8"]


def test_settings_applies_app_overrides(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(display_name="TestApp", version="1.2.3")

    assert settings.app.display_name == "TestApp"
    assert settings.app.version == "1.2.3"
