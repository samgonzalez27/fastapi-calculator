
"""Calculator logic separated for easy unit testing with logging hooks."""
from typing import Union
import logging

# Ensure logging config is applied early for modules that import this file
from . import logging_config  # noqa: F401

logger = logging.getLogger("calculator.operations")


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    logger.info("add called with a=%s, b=%s", a, b)
    result = a + b
    logger.debug("add result=%s", result)
    return result


def sub(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    logger.info("sub called with a=%s, b=%s", a, b)
    result = a - b
    logger.debug("sub result=%s", result)
    return result


def mul(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    logger.info("mul called with a=%s, b=%s", a, b)
    result = a * b
    logger.debug("mul result=%s", result)
    return result


def div(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    logger.info("div called with a=%s, b=%s", a, b)
    if b == 0:
        logger.error("division by zero attempted: a=%s, b=%s", a, b)
        raise ZeroDivisionError("division by zero")
    result = a / b
    logger.debug("div result=%s", result)
    return result
