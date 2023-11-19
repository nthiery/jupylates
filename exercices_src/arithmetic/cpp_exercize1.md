---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

```{code-cell}
---
editable: true
slideshow:
  slide_type: ''
tags: [hide-cell]
---
#include "jupyter_exercizer_helpers.hpp"
CONST A = RANDOM_INT(1,41);
CONST B = RANDOM_INT(1, 2); 
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

# Exercice: incrémentation

:::{admonition} Consigne

Quelle est la valeur de `R` après exécution du code suivant en C++?

:::

```{code-cell}
---
editable: true
slideshow:
  slide_type: ''
---
int R = A;
```

```{code-cell}
---
editable: true
slideshow:
  slide_type: ''
---
R = R + B;
```

```{code-cell}
---
tags: [output]
editable: true
nbgrader:
  grade: false
  grade_id: cell-ce41a6ebf1de8c4f
  locked: false
  schema_version: 3
  solution: true
  task: false
slideshow:
  slide_type: ''
---
int answer = A + B;
```

```{code-cell}
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
CHECK( R == answer );
```
