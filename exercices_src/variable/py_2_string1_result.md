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

### Objectif Pédagogique : comprendre la difference entre valeur et nom d'une variable de type string.

```{code-cell} ipython3
:editable: false
:tags: [hide-cell]

from jupyter_exercizer_helpers import RANDOM_CHOICE, CONST
```

```{code-cell} ipython3
:tags: [hide-cell, variable]

NAMEstr: CONST = RANDOM_CHOICE("Bob", "Barbara", "Pierre", "Paul", "Jeanne", "Camille")
NAMEstr
```

```{code-cell} ipython3
:tags: [hide-output, substitution]

NAME = NAMEstr
r = NAME
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
result = INPUT(NAMEstr)
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
