"""Central logging configuration for the calculator app.

This module ensures a single logging configuration is applied once. Importing
this module will configure the 'calculator' logger (and its children) to
log to stdout with a simple formatter. It avoids adding duplicate handlers.
"""
import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
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
