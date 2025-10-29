
"""Calculator logic separated for easy unit testing with logging hooks.

This module implements simple arithmetic functions used by the FastAPI
application. Each function is intentionally small and well-tested.
"""
from typing import Union
import logging

# Ensure logging config is applied early for modules that import this file.
# The import is for side-effects (configuring logging) and pylint would
# normally flag it as unused; disable that warning on this line.
from . import logging_config  # pylint: disable=unused-import

logger = logging.getLogger("calculator.operations")


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return the sum of ``a`` and ``b``.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        The arithmetic sum of ``a`` and ``b``.
    """
    logger.info("add called with a=%s, b=%s", a, b)
    result = a + b
    logger.debug("add result=%s", result)
    return result


def sub(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return ``a`` minus ``b``."""
    logger.info("sub called with a=%s, b=%s", a, b)
    result = a - b
    logger.debug("sub result=%s", result)
    return result


def mul(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return the product of ``a`` and ``b``."""
    logger.info("mul called with a=%s, b=%s", a, b)
    result = a * b
    logger.debug("mul result=%s", result)
    return result


def div(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return ``a`` divided by ``b``.

    Raises:
        ZeroDivisionError: If ``b`` is zero.
    """
    logger.info("div called with a=%s, b=%s", a, b)
    if b == 0:
        logger.error("division by zero attempted: a=%s, b=%s", a, b)
        raise ZeroDivisionError("division by zero")
    result = a / b
    logger.debug("div result=%s", result)
    return result
