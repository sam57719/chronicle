from __future__ import annotations

from importlib.metadata import PackageNotFoundError, metadata
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

__all__ = ["ApplicationInfo", "LicenseInfo"]


class LicenseInfo(BaseModel):
    """API licence information."""

    name: str = ""
    url: str | None = None


_PACKAGE_NAME = "menagerist"
_DEFAULT_DISPLAY_NAME = "Menagerist"


class _MenageristToolConfig(BaseSettings):
    """Settings from [tool.menagerist] in pyproject.toml."""

    model_config = SettingsConfigDict(
        frozen=True,
        pyproject_toml_table_header=("tool", _PACKAGE_NAME),
        populate_by_name=True,
    )

    display_name: Annotated[str, Field(alias="display-name")] = _DEFAULT_DISPLAY_NAME

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Load from [tool.menagerist] in pyproject.toml."""
        return (PyprojectTomlConfigSettingsSource(settings_cls),)


class ApplicationInfo(BaseModel):
    """Combined application metadata from importlib and pyproject.toml."""

    model_config = ConfigDict(frozen=True)

    name: str = _PACKAGE_NAME
    display_name: str = _DEFAULT_DISPLAY_NAME
    version: str = "0.0.0"
    description: str = ""
    license: LicenseInfo = Field(default_factory=LicenseInfo)

    @classmethod
    def from_package(cls) -> ApplicationInfo:
        """Load metadata from the installed package and pyproject.toml."""
        tool = _MenageristToolConfig()
        try:
            meta = metadata(_PACKAGE_NAME)
            urls = dict(
                entry.split(", ", 1) for entry in meta.get_all("Project-URL") or []
            )
            return cls(
                name=meta["Name"] or _PACKAGE_NAME,
                display_name=tool.display_name,
                version=meta["Version"] or "0.0.0",
                description=meta["Summary"] or "",
                license=LicenseInfo(
                    name=meta["License-Expression"],
                    url=urls.get("License"),
                ),
            )
        except PackageNotFoundError:
            return cls(display_name=tool.display_name)
