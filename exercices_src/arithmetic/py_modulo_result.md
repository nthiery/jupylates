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

### Objectif Pédagigique : reste de la division entière.

```{code-cell} ipython3
:editable: false
:tags: [hide-cell]

from jupyter_exercizer_helpers import RANDOM_CHOICE, CONST
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

I1: CONST = RANDOM_CHOICE(3, 5, 7)
I1
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

I3: CONST = RANDOM_CHOICE(1, 2, 4, 8, 11, 13, 16, 17, 19, 22)
I3
```

```{code-cell} ipython3
:tags: [hide-output, substitution]

r = I3 % I1
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
result = INPUT(I3 % I1)
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
