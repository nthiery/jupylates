from typing import Any
from random import randint


CONST = Any


def INPUT(default: Any) -> Any:
    return default


def RANDOM_INT(min: int, max: int):
    return randint(min, max+1)
