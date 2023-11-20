---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

### Objectif pédagogique : altérnative aux parenthèses.

```{code-cell}
:editable: false
:tags: [hide-cell]

from jupyter_exercizer_helpers import RANDOM_INT, CONST
```

+++

```{code-cell}
---
tags: [hide-cell, variable]
---

I1: CONST = RANDOM_INT(1, 5)
I2: CONST = RANDOM_INT(1, 7)
I3: CONST = RANDOM_INT(1, 5)
```

+++

```{code-cell}
---
tags: [hide-output, substitution]
---
I = I2 - I1
J = I3 + I2
K = I * J
N = I2 - I1 * I3 + I2
r = K == N
```

+++

:::{admonition} Consigne

Assigner la valeur attendue de r à la variable result

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
## BEGIN SOLUTION
## Votre solution ici
result = r;
## END SOLUTION
```

+++

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
assert result == r
```
