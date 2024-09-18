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
learning_objective: 'échange de variables'
---

```{code-cell} ipython3
:tags: [hide-cell, substitutions]

import random
from jupylates.jupylates_helpers import SUBSTITUTE

SUBSTITUTE(
	I1 = random.randint((1, 7),
	I2 = random.randint(8, 15)
)
```

:::{admonition} Consigne

Quelle est la valeur attendue de `r` après exécution du code suivant?

:::

```{code-cell} ipython3
X = I1
Y = I2

Z = X
X = Y
Y = Z
r = Y
```

```{code-cell} ipython3
:tags: [hide-cell]

SOLUTION = I1
del r, X, Y, Z
```

```{code-cell} ipython3
:tags: [solution]

I1
```

```{code-cell} ipython3
:tags: [test, hide-cell]

assert _ == SOLUTION
```
