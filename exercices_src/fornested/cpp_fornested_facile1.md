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

### Objectif Pédagogique : comprendre les boucles for imbriquées

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

CONST I1 = RANDOM_INT(0, 5);
CONST LongueurI = RANDOM_INT(1, 3);
CONST I2 = I1 + LongueurI;

CONST J1 = RANDOM_INT(0, 5);
// pour qu'ils ne soient pas tous les deux grands, sinon l'exo est interminable:
CONST LongueurJ = 4 - LongueurI;
CONST J2 = J1 + LongueurJ;

```


```{code-cell}
for ( int I = I1; I <= I2; I++ ) {
    for ( int J = J1; J <= J2; J++) {
        int r1 = J;
        int r2 = I;
    }
}
```

:::{admonition} Consigne

Quelle est la valeur attendue de `r1` et `r2`?

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
int result1 = INPUT(
   /// BEGIN SOLUTION
   J
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
int result2 = INPUT(
   /// BEGIN SOLUTION
   I
   /// END SOLUTION
);
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
CHECK( result1 == r1 );
CHECK( result2 == r2 );
```