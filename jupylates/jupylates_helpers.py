import json
from typing import Any
from random import randint, choice


CONST = Any


def INPUT(default: Any) -> Any:
    return default


def RANDOM_INT(min: int, max: int) -> int:
    return randint(min, max)


def RANDOM_CHOICE(*args: Any) -> Any:
    r"""
    Return a random element of `args`

        >>> RANDOM_CHOICE("alice", "bob", "charlie")  # doctest: +SKIP
        'charlie'

        >>> RANDOM_CHOICE("alice")
        'alice'
    """
    return choice(args)


def SUBSTITUTE(**args: Any) -> str:
    return json.dumps({key: str(value) for key, value in args.items()})
