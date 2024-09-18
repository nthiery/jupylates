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
learning_objective: 'différence entre accumulateur et simple affectation'
---

```{code-cell} ipython3
:tags: [hide-cell, substitutions]

from jupylates.jupylates_helpers import SUBSTITUTE
import random

SUBSTITUTE(I1=random.randint(5, 17))
```

:::{admonition} Consigne

Quelles sont les valeurs attendues de `x` et `y` après exécution du
code suivant?

:::

```{code-cell} ipython3
x = 0
y = 0
while ( x < I1 ):
    x = x + 1
    y = 1
```

```{code-cell} ipython3
:tags: [hide-cell]

SOLUTION_x = x
SOLUTION_y = y
del x, y
```

```{code-cell} ipython3
:tags: [solution, hide-output]

I1
```

```{code-cell} ipython3
:tags: [solution, hide-output]

1
```

```{code-cell} ipython3
:tags: [test, hide-cell]

assert __ == SOLUTION_x
assert _ == SOLUTION_y
```
