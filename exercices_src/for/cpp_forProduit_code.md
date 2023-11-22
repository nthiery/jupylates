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

### Objectif Pédagigique : boucle for avec accumulateur.

```{code-cell}
:editable: false
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

```{code-cell}
:tags: [hide-cell, variable]

CONST I1 = RANDOM_INT(1, 6);
CONST I2 = I1 + RANDOM_INT(10,12);
```

:::{admonition} Consigne

Écrire le code permettant de mettre dans la variable p
le produit des entiers compris entre I1 et I2 inclus.

:::

```{code-cell}
:editable: true

long int p;
```

```{code-cell}
---
editable: true
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
// BEGIN SOLUTION
p = 1;
for (int i = I1; i <= I2; i++)
    p = p * i;
// END SOLUTION
```

```{code-cell}
---
editable: false
nbgrader:
  grade: true
  grade_id: check
  locked: true
  points: 1
  schema_version: 3
  solution: false
tags: [hide-cell]
---
long int result = 1;
for (int i = I1; i <= I2; i++)
    result = result * i;
CHECK( result == p );
```
