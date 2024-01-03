---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: myst
kernelspec:
   display_name: Python 3 (ipykernel)
   language: python
   name: python3
---

### Objectif pédagogique : différence entre accumulateur et simple affectation

```{code-cell} python
---
editable: false
tags: [hide-cell]
---
from jupylates_helpers import RANDOM_INT, CONST

I1: CONST = RANDOM_INT(5, 17);
```

```{code-cell} python
x = 0
y = 0
while ( x < I1 ):
    x = x + 1
    y = 1
```

:::{admonition} Consigne

Quelle est la valeur attendue de `x` et `y`?

:::

```{code-cell}
---
editable: true
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

```{code-cell}
---
editable: true
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

```{code-cell}
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
assert resultx == x
assert resulty == y
```
