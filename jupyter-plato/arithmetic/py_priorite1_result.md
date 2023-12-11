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

### Objectif pédagogique : priorité des opérations.

```{code-cell} python
---
editable: false
tags: [hide-cell]
---
from jupyter_exercizer_helpers import RANDOM_INT, CONST
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
---
I1: CONST = RANDOM_INT(1, 7)
I1
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
---
I2: CONST = RANDOM_INT(5, 12)
I2
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
---
I3: CONST = RANDOM_INT(1, 7)
I3
```

+++

```{code-cell} python
---
tags: [hide-output,substitution]
---

r = I2 + I1 * I3

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
    I2 + I1 * I3
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
