"""Logging configuration helpers."""

from __future__ import annotations

import logging

_LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"

_configured = False


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging for the application.

    Args:
        level: Logging level name (for example ``"INFO"`` or ``"DEBUG"``).
    """

    global _configured
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format=_LOG_FORMAT)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger, configuring logging on first use.

    Args:
        name: The logger name, typically ``__name__``.

    Returns:
        A configured :class:`logging.Logger`.
    """

    if not _configured:
        configure_logging()
    return logging.getLogger(name)
