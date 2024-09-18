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
learning_objective: 'gérer les tranches de tableaux numpy'
---

```{code-cell} ipython3
:tags: [hide-cell]

from random import randint
NROWS = randint(2, 6)
NCOLUMNS = randint(10, 12)
I = randint(1, NROWS)
import numpy as np
T = np.array(range(NROWS*NCOLUMNS)).reshape(NROWS, NCOLUMNS)
```

:::{admonition} Consigne

Soit T le tableau numpy suivant à {eval}`NROWS` lignes et {eval}`NCOLUMNS` colonnes:
```
{eval}` T `
```
Extraire la {eval}`I` ème ligne du tableau T.

:::

```{code-cell} ipython3
:tags: [solution]

```

```{code-cell} ipython3
:tags: [hide-cell]

answer = _
SOLUTION = T[I-1,:]
```

```{code-cell} ipython3
:tags: [test, hide-cell]

assert answer.shape == SOLUTION.shape
assert np.all(answer == SOLUTION)
```
