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

### Objectif Pédagigique : boucle for avec accumulateur.

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
I1: CONST = RANDOM_INT(1, 6)
I2: CONST = I1 + RANDOM_INT(10,12)
```

+++

:::{admonition} Consigne

Écrire le code permettant de mettre dans la variable p
le produit des entiers compris entre I1 et I2 inclus.

:::

```{code-cell} python
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: true}
---
### BEGIN SOLUTION
p = 1;
for i in range(I1, I2+1):
    p = p * i
### END SOLUTION
```

+++

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: false}
---
result = 1;
for i in range(I1, I2+1):
    result = result * i
assert result == p
```
