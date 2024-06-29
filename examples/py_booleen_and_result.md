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

### Objectif pédagogique : opérateur `and`

```{code-cell} ipython3
:tags: [hide-cell, substitutions]

from jupylates.jupylates_helpers import SUBSTITUTE
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

```{code-cell} ipython3
X = I1
if X >= 0 and X <= 2 :
    A = True
else:
    A = False
```

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
### BEGIN SOLUTION
R
### END SOLUTION
```

```{code-cell} ipython3
:tags: [hide-cell]

result = _
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
assert result == R
```
