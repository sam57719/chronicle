"""Application bootstrap helpers.

Small lifecycle helpers (startup/shutdown). Logging configuration lives in
`app.shared.logging_` so the bootstrap module remains focused on lifecycle
behaviour and does not mix responsibilities.
"""

from typing import TYPE_CHECKING

import structlog

from app.shared.logging_ import configure_logging

if TYPE_CHECKING:
    from app.shared.config import Settings

__all__ = ["shutdown", "startup"]


async def startup(settings: Settings) -> None:
    """Application startup hook.

    Import logging_ helpers lazily to avoid import cycles and keep bootstrap
    lightweight for tests that don't require logging_ configuration.
    """
    configure_logging(settings.logging.level, settings.logging.mode)
    logger = structlog.get_logger("bootstrap")
    logger.info("application.startup")
    logger.debug(
        "application.startup.settings", settings=settings.model_dump(mode="json")
    )


async def shutdown(settings: Settings) -> None:
    """Application shutdown hook.

    Perform tidy-up tasks and emit a shutdown message.
    """
    logger = structlog.get_logger("bootstrap")
    logger.info("application.shutdown")
