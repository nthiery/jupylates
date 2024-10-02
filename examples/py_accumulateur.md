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

from jupylates.jupylates_helpers import SUBSTITUTE, INPUT_INT, assertEqual
import random

SUBSTITUTE(I1=random.randint(5, 17))
```

:::{admonition} Consigne
Quelles sont les valeurs attendues de `x` et `y` après exécution du
code suivant?
:::

```{code-cell}
x = 0
y = 0
while ( x < I1 ):
    x = x + 1
    y = 1
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

solution_x, answer_x = INPUT_INT("x", x)
solution_y, answer_y = INPUT_INT("y", y)

assertEqual(answer_x, solution_x)
assertEqual(answer_y, solution_y)
```
