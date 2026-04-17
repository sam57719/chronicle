"""Structured logging_ configuration helpers.

This module contains the logic to configure structlog and expose a
convenience `get_logger()` function. It is intentionally small so other
modules (including `bootstrap`) can import the logging_ helpers without
dragging in unrelated lifecycle code.
"""

import logging
import sys
from typing import Any

import structlog

__all__ = ["configure_logging"]

from app.shared.logging_.semantic_sorter import SemanticSorter


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the standard-library logging_ and structlog.

    Args:
        level: Log level for the stdlib root logger.
    """
    common_processors: list[Any] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        SemanticSorter(order=["timestamp", "event", "level", "logger"]),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ]

    logging.basicConfig(stream=sys.stdout, level=level, format="%(message)s")

    structlog.configure(
        processors=common_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
