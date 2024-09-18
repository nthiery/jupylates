import random
import re
from typing import Any, Callable, Dict, List, Tuple

from .jupylates_helpers import RANDOM_INT, RANDOM_CHOICE

STRING_QUOTE = '"'
VECTOR_OPEN = "{"
VECTOR_CLOSE = "}"


def_regexp = {
    "C++": r"CONST\s+(\w+)\s+=\s+(.*?);?\s*$",
    "python": r"(\w+):\s+CONST\s+=\s+(.*?);?\s*$",
}
for language in ["C++11", "C++14", "C++17"]:
    def_regexp[language] = def_regexp["C++"]


def to_language(value: Any) -> str:
    """
    Return `value` as a string representing a C++ constant

    .. TODO:: make the output language configurable

        >>> to_language(3)
        '3'
        >>> to_language("alice")
        '"alice"'
        >>> to_language([1,2,3])
        '{1, 2, 3}'
        >>> to_language([[1,2],["alice", "bob"]])
        '{{1, 2}, {"alice", "bob"}}'
    """
    if isinstance(value, str):
        if value == "REF":
            return "&"
        if value == "VAL":
            return ""
        return STRING_QUOTE + value + STRING_QUOTE
    elif isinstance(value, list):
        return VECTOR_OPEN + ", ".join(to_language(v) for v in value) + VECTOR_CLOSE
    else:
        return str(value)


def RANDOM_VECTOR(n: int, generator: Callable, *args: Any) -> List:
    r"""
    Return a random vector of length `n` and whose elements are
    generated by calling `generator(*args)`

    This return a random vector of integers of length 5, with
    elements between 1 and 3:

        >>> RANDOM_VECTOR(5, RANDOM_INT, 1, 3) # doctest: +SKIP
        [3, 1, 2, 1, 3]

        >>> RANDOM_VECTOR(5, RANDOM_INT, 1, 1)
        [1, 1, 1, 1, 1]
    """
    return [generator(*args) for i in range(n)]


def RANDOM_VALOUREF() -> str:
    r"""
    pas sur que ce soit la meilleur des methodes....
    """
    return str(random.choice(["REF", "VAL"]))


locals = {
    "RANDOM_INT": RANDOM_INT,
    "RANDOM_CHOICE": RANDOM_CHOICE,
    "RANDOM_VECTOR": RANDOM_VECTOR,
    "RANDOM_VALOUREF": RANDOM_VALOUREF,
}

test_code = """CONST N = RANDOM_INT(3,3);
CONST M = RANDOM_INT(4,4);
CONST V = RANDOM_VECTOR(N, RANDOM_INT, 5, 5);
CONST VV = RANDOM_VECTOR(N, RANDOM_VECTOR, M, RANDOM_INT, 1, 1);
int main () {
    int a = N + M;
    vector<int> v = V;
    vector<vector<int>> vv = VV;
}"""


class Randomizer:
    def __init__(self, language: str = "C++") -> None:
        consts = {}
        consts["R"], consts["S"], consts["T"] = random.sample("rst", 3)
        consts["X"], consts["Y"], consts["Z"] = random.sample("xyz", 3)
        consts["I"], consts["J"], consts["K"], consts["N"] = random.sample("ijkn", 4)
        consts["PLUSOUMOINS"] = str(random.choice(["+", "-"]))
        consts["NAME"] = str(
            random.choice(
                ["Alexandre", "Yasmine", "Albert", "Alice", "Antoine", "Anna"]
            )
        )
        self.consts = consts

        self.def_regexp = re.compile(def_regexp[language])

    def randomize(self, text: str, is_code: bool = True) -> str:
        result = []
        for line in text.splitlines():
            pattern = re.compile(r"\b(" + "|".join(self.consts.keys()) + r")\b")
            if is_code:
                match = re.match(self.def_regexp, line)
            else:
                match = None
            if match:
                # Define new constant
                variable, value = match.groups()
                # Substitutes all constants in the value
                value = pattern.sub(lambda i: self.consts[i.group()], value)
                # Evaluates the value in a context containing all the RANDOM_*
                # functions
                self.consts[variable] = to_language(eval(value, {}, locals))
            else:
                # Substitutes all constants
                line = pattern.sub(lambda i: self.consts[i.group()], line)
                result.append(line)
        return "\n".join(result)


def randomize_code(code: str) -> Tuple[str, Dict]:
    r"""
    Randomize the given code

    Examples:

        >>> import random
        >>> random.seed(0)
        >>> randomize_code("int XX=3;")[0]
        'int XX=3;'
        >>> randomize_code("int X=3; int Y=4; int Z=5;")[0]
        'int z=3; int x=4; int y=5;'
        >>> randomize_code("I, J, K, N")[0]
        'n, k, j, i'
        >>> randomize_code("int X=1;\nint Y=2;")[0]
        'int z=1;\nint y=2;'

        >>> print(test_code)
        CONST N = RANDOM_INT(3,3);
        CONST M = RANDOM_INT(4,4);
        CONST V = RANDOM_VECTOR(N, RANDOM_INT, 5, 5);
        CONST VV = RANDOM_VECTOR(N, RANDOM_VECTOR, M, RANDOM_INT, 1, 1);
        int main () {
            int a = N + M;
            vector<int> v = V;
            vector<vector<int>> vv = VV;
        }
        >>> print(randomize_code(test_code)[0])
        int main () {
            int a = 3 + 4;
            vector<int> v = {5, 5, 5};
            vector<vector<int>> vv = {{1, 1, 1, 1}, {1, 1, 1, 1}, {1, 1, 1, 1}};
        }
    """
    randomizer = Randomizer()
    code = randomizer.randomize(code)
    return code, randomizer.consts
