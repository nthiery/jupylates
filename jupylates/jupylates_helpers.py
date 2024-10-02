import json
from typing import Any, Optional, Tuple, TypeVar
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
    import __main__

    __main__.__dict__.update(args)
    return json.dumps({key: str(value) for key, value in args.items()})


T = TypeVar("T", int, float, str, Any)


def INPUT_EXPR[T](label: str, solution: T, answer: Optional[T]=None) -> Tuple[T,T]:
    if answer is None:
        answer = solution
    return solution, answer


INPUT_INT = INPUT_EXPR
INPUT_FLOAT = INPUT_EXPR
INPUT_TEXT = INPUT_EXPR
INPUT_BOOL = INPUT_EXPR


def assertEqual(answer: Any, solution: Any) -> None:
    if answer != solution:
        raise ValueError(f"Réponse {answer} incorrecte; valeur attendue: {solution}")
