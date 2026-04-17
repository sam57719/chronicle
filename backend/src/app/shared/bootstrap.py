"""Application bootstrap helpers.

Small lifecycle helpers (startup/shutdown). Logging configuration lives in
`app.shared.logging_` so the bootstrap module remains focused on lifecycle
behaviour and does not mix responsibilities.
"""

from __future__ import annotations

import logging

__all__ = ["shutdown", "startup"]

import structlog

from app.shared.logging_ import configure_logging


async def startup() -> None:
    """Application startup hook.

    Import logging_ helpers lazily to avoid import cycles and keep bootstrap
    lightweight for tests that don't require logging_ configuration.
    """
    configure_logging()
    logger = structlog.get_logger("bootstrap")
    logger.info("application.startup")


async def shutdown() -> None:
    """Application shutdown hook.

    Perform tidy-up tasks and emit a shutdown message.
    """
    logger = structlog.get_logger("bootstrap")
    logger.info("application.shutdown")
    logging.shutdown()
