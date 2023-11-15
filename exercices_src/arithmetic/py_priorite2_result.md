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

### Objectif Pédagogique : priorité des opérations.

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
I1 = RANDOM_INT(1, 5)
I1
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
I2 = RANDOM_INT(1, 3)
I2
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
I3 = RANDOM_INT(1, 7)
I3
```

+++

```{code-cell} python
---
tags: [hide-output,substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

r = (I2 PLUSOUMOINS I1) * I3

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
