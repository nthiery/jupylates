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

### Objectif Pédagogique : échange de variable correct.

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
I1: CONST = RANDOM_INT(0, 7)
I1
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
---
I2: CONST = RANDOM_INT(8, 15)
I2
```

+++

```{code-cell} python
---
tags: [hide-output, substitution]
---

X = I1
Y = I2

Z = X
X = Y
Y = Z
r = Y
```

+++

:::{admonition} Consigne

Assigner la valeur attendue de r à la variable result

:::

```{code-cell} python
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: true}
---
## BEGIN SOLUTION
## Votre solution ici
result = Y
## END SOLUTION
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
