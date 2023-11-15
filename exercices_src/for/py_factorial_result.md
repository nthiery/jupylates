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

### Objectif Pédagigique : comprendre une factorielle avec une boucle for

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
from randomization import RANDOM_INT
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
N0 = RANDOM_INT(3, 5) + 1
## Ne pas randomiser le nom de variable pour l'indice k, sinon risque qu'on tombe sur n, qui existe déjà dans ce code.
## (Ou alors remplacer n par m, puis randomiser le nom de variable de l'indice k ?)
N0
```

+++

```{code-cell} python
---
tags: [hide-output, substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
n = N0
r = 1

for k in range(1, n) :
    r = r * k
```

+++

Assigner la valeur attendue de r à la variable result

```{code-cell} python
---
editable: true
tags: [answer]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
## Votre solution ici
```

+++

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: true}
---
assert result == r
```
