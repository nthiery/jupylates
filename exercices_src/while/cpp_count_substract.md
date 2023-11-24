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

### Objectif Pédagogique : boucle while avec compteur (ici calcul du quotient).

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;

CONST I1 = RANDOM_INT(20, 37);
CONST I2 = RANDOM_INT(5, 10);
```

```{code-cell}
int n = I1;
int i = 0;
while (n > I2) {
    n = n - I2;
    i = i + 1;
}
```

:::{admonition} Consigne

Quelle est la valeur attendue de i et n?

:::

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
int resulti = INPUT(
    /// BEGIN SOLUTION
    i
    /// END SOLUTION
);
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
int resultn = INPUT(
    /// BEGIN SOLUTION
    n
    /// END SOLUTION
);
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
CHECK( resulti == i );
CHECK( resultn == n );
```
