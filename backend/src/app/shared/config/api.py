"""API-specific configuration settings."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.shared.types import CSV, ValidatedNetworkHostStr  # noqa: TC001


class APISettings(BaseSettings):
    """Settings for the API entrypoint."""

    model_config = SettingsConfigDict(
        frozen=True,
    )

    trusted_hosts: Literal["*"] | CSV[ValidatedNetworkHostStr] = Field("*")
    access_log_enabled: bool = True
