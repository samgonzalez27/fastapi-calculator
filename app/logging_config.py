"""Central logging configuration for the calculator app.

Provides a single function, :func:`configure_logging`, that applies a
stream-based handler and a consistent formatter to the ``calculator``
logger. Importing this module will configure logging once. The function
is idempotent and safe to call multiple times.
"""
import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the ``calculator`` logger to write to stdout.

    The function is idempotent: calling it multiple times will not add
    duplicate handlers.

    Args:
        level: The logging level to set on the configured logger.
    """
    root_logger = logging.getLogger("calculator")
    # Only configure if no handlers are present to avoid duplicate logs
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


# Configure at import time so modules importing calculator get logging configured
configure_logging()
