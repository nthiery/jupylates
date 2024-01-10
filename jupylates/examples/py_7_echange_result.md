---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

### Objectif pédagogique : échange de variable correct.

```{code-cell} ipython3
:editable: false
:tags: [hide-cell]

from jupylates.jupylates_helpers import RANDOM_INT, CONST, INPUT
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

I1: CONST = RANDOM_INT(0, 7)
I1
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

I2: CONST = RANDOM_INT(8, 15)
I2
```

```{code-cell} ipython3
:tags: [hide-output, substitution]

X = I1
Y = I2

Z = X
X = Y
Y = Z
r = Y
```

:::{admonition} Consigne

Quelle est la valeur attendue de r?

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
result = INPUT(
    ### BEGIN SOLUTION
    Y
    ### END SOLUTION
)
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
assert result == r
```
