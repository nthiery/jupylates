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

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
tags: [hide-cell]
---
from jupyter_exercizer_helpers import *
A: CONST = RANDOM_INT(1,10)
B: CONST = RANDOM_INT(1,10)
```

+++ {"slideshow": {"slide_type": ""}}

# Exercise : incrémentation

:::{admonition} Consigne

Quelle est la valeur de `R` après exécution du code suivant?

:::

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
R = A;
```

```{code-cell} ipython3
---
slideshow:
  slide_type: ''
---
R = R + B;
```

```{code-cell} ipython3
---
tags: [output]
editable: true
nbgrader:
  grade: false
  grade_id: cell-a690d81bc0582465
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
---
answer = (A + B)
```

```{code-cell} ipython3
---
editable: true
nbgrader:
  grade: true
  grade_id: cell-5ab67643ff0e09b3
  locked: true
  points: 0
  schema_version: 3
  solution: false
  task: false
slideshow:
  slide_type: ''
tags: [hide-cell]
---
assert R == answer
```
