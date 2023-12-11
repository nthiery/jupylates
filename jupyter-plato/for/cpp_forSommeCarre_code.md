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

### Objectif pédagogique : boucle for avec accumulateur

```{code-cell}
:editable: false
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

```{code-cell}
:tags: [hide-cell, variable]

CONST I1 = RANDOM_INT(0, 7);
CONST I2 = RANDOM_INT(18, 26);
```

:::{admonition} Consigne

Écrivez ici le code permettant de mettre dans la variable `s`
la somme des carrés des entiers compris entre I1 et I2 inclus.

:::

```{code-cell}
:editable: true

int s;
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
/// BEGIN SOLUTION
s = 0;
for (int i = I1; i <= I2; i++)
    s = s + i*i;
/// END SOLUTION
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
int result = 0;
for (int i = I1; i <= I2; i++)
    result = result + i * i;
CHECK( result == s );
```
