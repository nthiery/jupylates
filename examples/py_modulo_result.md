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

### Objectif pédagogique : reste de la division entière

+++ {"tags": ["hide-cell"]}

:::{attention}

Il est facile de «tricher» sur cet exercice en copiant-collant
l'expression à évaluer.

:::

```{code-cell}
:tags: [hide-cell]

from jupylates.jupylates_helpers import RANDOM_CHOICE, CONST
I1: CONST = RANDOM_CHOICE(3, 5, 7)
I3: CONST = RANDOM_CHOICE(1, 2, 4, 8, 11, 13, 16, 17, 19, 22)
```

```{code-cell}
R = I3 % I1
```

```{code-cell}
:tags: [hide-cell]

solution = R
del R
```

:::{admonition} Consigne

Quelle est la valeur attendue de `R`?

:::

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
tags: [hide-output]
---
I3 % I1
```

```{code-cell}
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
assert _ == solution
```
