from typing import TYPE_CHECKING

import pytest

from app.shared.config import Settings, get_settings

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from app.shared.config.app_info import ApplicationInfo


def pytest_configure() -> None:
    """Disable loading the local .env during test runs."""
    from app.shared.config import Settings

    Settings.model_config["env_file"] = None


@pytest.fixture(autouse=True)
def clear_config_cache() -> Generator[None]:
    """Clear cached config reads between tests for deterministic behaviour."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def settings() -> Settings:
    """Provide application settings for tests."""
    return get_settings()


@pytest.fixture
def settings_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[..., Settings]:
    """Build settings with optional env and app overrides."""

    def build(
        *,
        env: dict[str, str] | None = None,
        name: str | None = None,
        display_name: str | None = None,
        version: str | None = None,
        description: str | None = None,
        license_name: str | None = None,
        license_url: str | None = None,
    ) -> Settings:
        if env:
            for key, value in env.items():
                monkeypatch.setenv(key, value)

        get_settings.cache_clear()
        current: Settings = get_settings()

        app_info: ApplicationInfo = current.app

        if name is not None:
            app_info = app_info.model_copy(update={"name": name})
        if display_name is not None:
            app_info = app_info.model_copy(update={"display_name": display_name})
        if version is not None:
            app_info = app_info.model_copy(update={"version": version})
        if description is not None:
            app_info = app_info.model_copy(update={"description": description})
        if license_name is not None or license_url is not None:
            license_update: dict[str, object] = {}
            if license_name is not None:
                license_update["name"] = license_name
            if license_url is not None:
                license_update["url"] = license_url

            app_info = app_info.model_copy(
                update={"license": app_info.license.model_copy(update=license_update)}
            )

        return current.model_copy(update={"app": app_info})

    return build
