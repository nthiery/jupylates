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
tags: [hidden]
---
from jupyter_exercizer_helpers import *
D: CONST = RANDOM_INT(1,10)
```

+++ {"slideshow": {"slide_type": ""}, "editable": true}

# Exercice : incrémentation

:::{admonition} Consigne

Quelle valeur doit avoir `R` avant l'exécution de ce code pour qu'il vaille 42 à la fin?

:::

```{code-cell} ipython3
---
answer: output
editable: true
nbgrader:
  grade: false
  grade_id: cell-b2b14bef0a5da1ca
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
---
R = INPUT(42-D)
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
R = R + D;
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
tags: [hidden]
---
assert R == 42
```
