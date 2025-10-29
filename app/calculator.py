"""Calculator logic separated for easy unit testing."""
from typing import Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b


def sub(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a - b


def mul(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a * b


def div(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
