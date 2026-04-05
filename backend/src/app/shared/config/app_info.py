from __future__ import annotations

from importlib.metadata import PackageNotFoundError, metadata

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
)

__all__ = ["ApplicationInfo", "ContactInfo", "LicenseInfo"]


class ContactInfo(BaseModel):
    """API contact information."""

    name: str = ""
    url: str = ""
    email: str = ""


class LicenseInfo(BaseModel):
    """API licence information."""

    name: str = "Apache-2.0"
    url: str = ""


class _MenageristToolConfig(BaseSettings):
    """Settings from [tool.menagerist] in pyproject.toml."""

    model_config = SettingsConfigDict(
        frozen=True,
        pyproject_toml_table_header=("tool", "menagerist"),
    )

    display_name: str = Field("Menagerist", alias="display-name")

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

    name: str = "menagerist"
    display_name: str = "Menagerist"
    version: str = "0.0.0"
    description: str = ""
    contact: ContactInfo = Field(default_factory=ContactInfo)
    license: LicenseInfo = Field(default_factory=LicenseInfo)

    @classmethod
    def from_package(cls) -> ApplicationInfo:
        """Load metadata from the installed package and pyproject.toml."""
        tool = _MenageristToolConfig()
        try:
            meta = metadata("menagerist")
            urls = dict(
                entry.split(", ", 1) for entry in meta.get_all("Project-URL") or []
            )
            return cls(
                name=meta["Name"] or "menagerist",
                display_name=tool.display_name,
                version=meta["Version"] or "0.0.0",
                description=meta["Summary"] or "",
                contact=ContactInfo(
                    name=meta["Author"] or "",
                    url=urls.get("Repository", ""),
                    email=meta["Author-email"] or "",
                ),
                license=LicenseInfo(
                    name=meta["License-Expression"] or "Apache-2.0",
                    url=urls.get("License", ""),
                ),
            )
        except PackageNotFoundError:
            return cls(display_name=tool.display_name)
