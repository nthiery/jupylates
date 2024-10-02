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

import random
from jupylates.jupylates_helpers import SUBSTITUTE, INPUT_INT, assertEqual

SUBSTITUTE(
    I1=random.choice([3, 5, 7]),
    I3=random.choice([1, 2, 4, 8, 11, 13, 16, 17, 19, 22]),
)
```

:::{admonition} Consigne
Quelle est la valeur de l'expression suivante?
:::

```{code-cell}
:tags: [hide-output]

I3 % I1
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

solution, answer = INPUT_INT("", _)

assertEqual(answer, solution)
```
