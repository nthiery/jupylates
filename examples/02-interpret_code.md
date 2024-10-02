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
	I1 = random.randint(1, 7),
	I2 = random.randint(8, 15)
)
```

:::{admonition} Instructions
What's the value of `r` after executing the following code?
:::

```{code-cell}
X = I1
Y = I2

Z = X
X = Y
Y = Z
r = Y
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

solution, answer = INPUT_INT("r", r)

assertEqual(answer, solution)
```
