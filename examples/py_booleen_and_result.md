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
:editable: false
:tags: [hide-cell]

from jupylates.jupylates_helpers import RANDOM_INT, CONST, INPUT
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

I1: CONST = RANDOM_INT(3, 9)
I1
```

```{code-cell} ipython3
:tags: [hide-output, substitution]

x = I1
if x >= 0 and x <= 2 :
    r = True
else:
    r = False
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
    r
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
