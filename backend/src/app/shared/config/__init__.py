from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.config.app_info import ApplicationInfo
from app.shared.config.logging_ import LoggingSettings

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Root application settings — composed of sub-settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="MG_",
        env_parse_enums=True,
        case_sensitive=False,
        extra="ignore",
    )

    app: ApplicationInfo = Field(default_factory=ApplicationInfo.from_package)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
