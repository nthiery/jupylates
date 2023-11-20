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

### Objectif pédagogique : altérnative aux parenthèses.

```{code-cell}
:editable: false
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

+++

```{code-cell}
:tags: [hide-cell, variable]

CONST I1 = RANDOM_INT(1, 5);
CONST I2 = RANDOM_INT(1, 7);
CONST I3 = RANDOM_INT(1, 5);
```

+++

```{code-cell}
:tags: [hide-output, substitution]

    int I, J, K, N;
    I = I2 - I1;
    J = I3 + I2;
    K = I * J;
    N = I2 - I1 * I3 + I2;
    bool r = K == N;
```

+++

:::{admonition} Consigne

Assigner la valeur attendue de r à la variable result

:::

```{code-cell}
:editable: true

bool result;
```

+++

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
// Votre solution ici
result = r;
// END SOLUTION
```

+++

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
CHECK( result == r );
```
