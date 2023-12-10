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

### Objectif pédagogique : accumulateur avec boucle for

```{code-cell} python
---
editable: false
tags: [hide-cell]
---
from jupyter_exercizer_helpers import RANDOM_INT, CONST
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
RINIT: CONST = RANDOM_INT(1, 7)
RINIT
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
IMAX: CONST = RANDOM_INT(2, 4) + 1
IMAX
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
---
r = RINIT
for I in range(1, IMAX) :
    r = r + I
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
