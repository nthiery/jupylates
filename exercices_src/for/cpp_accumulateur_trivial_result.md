---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: myst
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

### Objectif Pédagogique : accumulateur avec boucle for

```{code-cell} c++
---
editable: false
tags: [hide-cell]
---
#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
CONST RINIT = RANDOM_INT(1, 7);
RINIT
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
CONST IMAX = RANDOM_INT(2, 4);
IMAX
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
---
int r = RINIT;
for ( int I = 1; I <= IMAX ; I = I + 1 ) {
    r = r + I;
}
```

+++

:::{admonition} Consigne

Assigner la valeur attendue de r à la variable result

:::

```{code-cell} c++
---
editable: true
---
int result;
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
