from typing import TYPE_CHECKING

from app.shared.config import Settings

if TYPE_CHECKING:
    from collections.abc import Callable


def test_app_settings_default(settings_factory: Callable[..., Settings]) -> None:
    settings = settings_factory()

    assert isinstance(settings, Settings)
    assert settings.app.display_name == "Menagerist"


def test_settings_factory_overrides_app_metadata(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(app={"display_name": "TestApp", "version": "1.2.3"})

    assert settings.app.display_name == "TestApp"
    assert settings.app.version == "1.2.3"


def test_settings_factory_overrides_license(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(
        app={
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            }
        }
    )

    assert settings.app.license.name == "MIT"
    assert settings.app.license.url == "https://opensource.org/licenses/MIT"


def test_settings_factory_applies_env_overrides(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(env={"MG_API__ACCESS_LOG_ENABLED": "false"})

    assert settings.api.access_log_enabled is False


def test_settings_factory_combines_env_and_app_overrides(
    settings_factory: Callable[..., Settings],
) -> None:
    settings = settings_factory(
        env={"MG_API__ACCESS_LOG_ENABLED": "false"},
        app={"display_name": "TestApp"},
    )

    assert settings.api.access_log_enabled is False
    assert settings.app.display_name == "TestApp"
