---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell}
:tags: [hide-cell, substitutions]

from jupylates.jupylates_helpers import SUBSTITUTE, INPUT_BOOL, assertEqual
import random

I1 = random.randint(3, 9)

SUBSTITUTE(
    # Substitute the variable I1 by its value in the following cells
    I1=I1,
    # Substitute the variables A, B, C respectively by some permutation of a, b, c
    **dict(zip("ABC", random.sample("abc", 3))),
    # Same for X, Y, Z
    **dict(zip("XYZ", random.sample("xyz", 3))),
)
```

:::{admonition} Consigne
Quelle est la valeur attendue de `A` après exécution du code suivant?
:::

```{code-cell}
X = I1
if X >= 0 and X <= 2 :
    A = True
else:
    A = False
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

solution, answer = INPUT_BOOL("A", A)

assertEqual(answer, solution)
```
