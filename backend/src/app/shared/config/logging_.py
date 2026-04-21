from enum import StrEnum, auto

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    """Logging levels."""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class LoggingMode(StrEnum):
    """Logging modes."""

    HUMAN = auto()
    JSON = auto()


class LoggingSettings(BaseSettings):
    """Logging settings."""

    model_config = SettingsConfigDict(
        frozen=True,
    )

    level: LogLevel = LogLevel.INFO
    mode: LoggingMode = LoggingMode.JSON
