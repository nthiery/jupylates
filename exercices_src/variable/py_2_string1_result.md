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

### Objectif Pédagogique : comprendre la difference entre valeur et nom d'une variable de type string.

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
NAMEstr = RANDOM_CHOICE("Bob", "Barbara", "Pierre", "Paul", "Jeanne", "Camille")
NAMEstr
```

+++

```{code-cell} python
---
tags: [hide-output, substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

NAME = NAMEstr
r = NAME
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
