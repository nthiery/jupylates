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

### Objectif Pédagogique : opération "and".

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
CONST I1 = RANDOM_INT(3, 9);
I1
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
---

int x = I1;
bool r;
if ( x >= 0 and x <= 2 ) {
    r = true;
} else {
    r = false;
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
