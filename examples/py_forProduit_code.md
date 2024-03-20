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

### Objectif pédagogique : boucle for avec accumulateur

```{code-cell}
:tags: [hide-cell]

from jupylates.jupylates_helpers import RANDOM_INT, CONST, INPUT
I1: CONST = RANDOM_INT(1, 6)
I2: CONST = I1 + RANDOM_INT(10,12)
```

:::{admonition} Consigne

Écrire le code permettant de mettre dans la variable `p`
le produit des entiers compris entre I1 et I2 inclus.

:::

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
### BEGIN SOLUTION
p = 1;
for i in range(I1, I2+1):
    p = p * i
### END SOLUTION
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
result = 1;
for i in range(I1, I2+1):
    result = result * i
assert result == p
```
