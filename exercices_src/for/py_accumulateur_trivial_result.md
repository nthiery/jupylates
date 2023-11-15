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

### Objectif Pédagogique : accumulateur avec boucle for

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
from randomization import RANDOM_INT
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
RINIT = RANDOM_INT(1, 7)
RINIT
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
IMAX = RANDOM_INT(2, 4) + 1
IMAX
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
r = RINIT
for I in range(1, IMAX) :
    r = r + I
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
