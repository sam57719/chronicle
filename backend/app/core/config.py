"""Configuration module."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from the environment."""

    DATABASE_URL: str = "sqlite+aiosqlite:///menagerist.db"


settings = Settings()
