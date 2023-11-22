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

### Objectif Pédagigique : comprendre une factorielle avec une boucle for

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
CONST N0 = RANDOM_INT(3, 5);
// Ne pas randomiser le nom de variable pour l'indice k, sinon risque qu'on tombe sur n, qui existe déjà dans ce code.
// (Ou alors remplacer n par m, puis randomiser le nom de variable de l'indice k ?)
N0
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
---
int n, r;
n = N0;
r = 1;

for ( int k = 1; k <= n; k++ ) {
    r = r * k;
}
```

+++

:::{admonition} Consigne

Quelle est la valeur attendue de r?

:::

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
int result = INPUT(r);
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
