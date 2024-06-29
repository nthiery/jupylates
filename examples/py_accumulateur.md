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

### Objectif pédagogique : différence entre accumulateur et simple affectation

```{code-cell} ipython3
:tags: [hide-cell]

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
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
resultx = INPUT(
    ### BEGIN SOLUTION
    I1
    ### END SOLUTION
)
```

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
resulty = INPUT(
    ### BEGIN SOLUTION
    1
    ### END SOLUTION
)
```

```{code-cell} ipython3
---
nbgrader:
  grade: true
  grade_id: check
  locked: true
  points: 1
  schema_version: 3
  solution: false
tags: [hide-cell]
---
assert resultx == x
assert resulty == y
```
