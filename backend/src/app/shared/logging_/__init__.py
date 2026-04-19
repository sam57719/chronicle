"""Structured logging_ configuration helpers.

This module contains the logic to configure structlog and expose a
convenience `get_logger()` function. It is intentionally small, so other
modules (including `bootstrap`) can import the logging_ helpers without
dragging in unrelated lifecycle code.
"""

from typing import Any

import structlog

from app.shared.config.logging_ import LoggingMode, LogLevel
from app.shared.logging_.semantic_sorter import SemanticSorter

__all__ = ["configure_logging"]


def _level_value(level: LogLevel) -> int:
    """Map configured log levels to structlog filtering values."""
    return {
        LogLevel.DEBUG: 10,
        LogLevel.INFO: 20,
        LogLevel.WARNING: 30,
        LogLevel.ERROR: 40,
        LogLevel.CRITICAL: 50,
    }[level]


def _base_processors() -> list[Any]:
    """Processors shared by both development and production modes."""
    return [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]


def configure_logging(
    level: LogLevel = LogLevel.INFO,
    mode: LoggingMode = LoggingMode.JSON,
) -> None:
    """Configure structlog for development or production output.

    Args:
        level: Minimum log level for emitted events.
        mode: Output format mode.
    """
    wrapper_class = structlog.make_filtering_bound_logger(_level_value(level))

    match mode:
        case LoggingMode.HUMAN:
            processors = [
                *_base_processors(),
                structlog.dev.ConsoleRenderer(),
            ]
        case LoggingMode.JSON:
            processors = [
                *_base_processors(),
                structlog.processors.dict_tracebacks,
                SemanticSorter(
                    order=["timestamp", "event", "level", "logger", "request_id"]
                ),
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ]

    structlog.configure(
        wrapper_class=wrapper_class,
        processors=processors,
        cache_logger_on_first_use=True,
    )
