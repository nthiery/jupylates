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

### Objectif pédagogique : gérer les tranches de tableaux numpy

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
---
editable: true
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---

```

```{code-cell} ipython3
:tags: [hide-cell]

answer = _
solution = T[I-1,:]
answer
```

```{code-cell} ipython3
---
editable: false
nbgrader:
  grade: true
  grade_id: check
  locked: true
  points: 1
  schema_version: 3
  solution: false
tags: [hide-cell]
---
assert answer.shape == solution.shape
assert np.all(answer == solution)
```
