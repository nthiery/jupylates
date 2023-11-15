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

### Objectif Pédagogique : division entière.

```{code-cell} python
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
from randomization import RANDOM_CHOICE
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
I1 = RANDOM_CHOICE(3, 5, 7)
I1
```

+++

```{code-cell} python
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
I3 = RANDOM_CHOICE(1, 2, 4, 8, 11, 13, 16, 17, 19, 22)
I3
```

+++

```{code-cell} python
---
tags: [hide-output, substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

r = int(I3 / I1)
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
