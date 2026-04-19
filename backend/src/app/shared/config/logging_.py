from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    """Logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingMode(StrEnum):
    """Logging modes."""

    HUMAN = "human"
    JSON = "json"


class LoggingSettings(BaseSettings):
    """Logging settings."""

    model_config = SettingsConfigDict(
        frozen=True,
    )

    level: LogLevel = LogLevel.INFO
    mode: LoggingMode = LoggingMode.JSON
