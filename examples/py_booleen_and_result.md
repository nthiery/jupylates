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

### Objectif pédagogique : opération "and".

```{code-cell} python
---
editable: false
tags: [hide-cell]
---
from jupylates.jupylates_helpers import RANDOM_INT, CONST, INPUT
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
---
I1: CONST = RANDOM_INT(3, 9)
I1
```

+++

```{code-cell} python
---
tags: [hide-output, substitution]
---

x = I1
if x >= 0 and x <= 2 :
    r = True
else:
    r = False

```

+++

:::{admonition} Consigne

Quelle est la valeur attendue de r?

:::

```{code-cell} python
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: true}
---
result = INPUT(
    ### BEGIN SOLUTION
    r
    ### END SOLUTION
)
```

+++

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: false}
---
assert result == r
```
