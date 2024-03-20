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

### Objectif pédagogique : déclarer une variable

```{code-cell} ipython3
:tags: [hide-cell]

from random import randint
I1 = randint(1,10)
```

:::{admonition} Consigne

Déclarez une variable entière `R` et affectez lui la valeur {eval}`I1`.

:::

```{code-cell} ipython3
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
R = I1
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
assert R == I1
```
