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
I1: CONST = RANDOM_INT(0, 7)
I2: CONST = RANDOM_INT(18, 26)
```

+++

:::{admonition} Consigne

Ecrire ici le code permettant de mettre dans la variable s
la somme des carrés des entiers compris entre I1 et I2 inclus.

:::

```{code-cell} python
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: true}
---
## BEGIN SOLUTION
## Votre solution ici
s = 0
for i in range(I1, I2+1):
    s = s + i * i
## END SOLUTION
```

+++

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: false}
---
result = 0
for i in range(I1, I2+1):
    result = result + i * i
assert result == s
```
