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
learning_objective: 'reste de la division entière'
---

+++ {"tags": ["hide-cell"]}

:::{attention}

Il est facile de «tricher» sur cet exercice en copiant-collant
l'expression à évaluer.

:::

```{code-cell}
:tags: [hide-cell, substitutions]

import random
from jupylates.jupylates_helpers import SUBSTITUTE

SUBSTITUTE(
    I1=random.choice([3, 5, 7]),
    I3=random.choice([1, 2, 4, 8, 11, 13, 16, 17, 19, 22]),
)
```

```{code-cell}
R = I3 % I1
```

```{code-cell}
:tags: [hide-cell]

SOLUTION = R
del R
```

:::{admonition} Consigne

Quelle est la valeur attendue de `R`?

:::

```{code-cell}
:tags: [answer, hide_output]

I3 % I1
```

```{code-cell}
:tags: [test, hide-cell]

assert _ == SOLUTION
```
