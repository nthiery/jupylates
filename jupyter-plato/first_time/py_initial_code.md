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

### Objectif pédagogique : savoit déclarer une variable.

```{code-cell}
:editable: false
:tags: [hide-cell]

from jupyter_exercizer_helpers import RANDOM_INT, CONST
```

+++

```{code-cell}
:tags: [hide-cell, variable]

I1: CONST = RANDOM_INT(1,10);
```

+++

:::{admonition} Consigne

Déclarez une variable entière r et affectez lui la valeur I1.

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
### BEGIN SOLUTION
r = I1
### END SOLUTION
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
assert r == I1
```
