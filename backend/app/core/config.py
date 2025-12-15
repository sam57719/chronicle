"""Configuration module."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from the environment."""

    DATABASE_URL: str


settings = Settings()
