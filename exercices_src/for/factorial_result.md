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
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
#include <iostream>
#include "randomization.h"
using namespace std;

CONST N0 = RANDOM_INT(3, 5);
// Ne pas randomiser le nom de variable pour l'indice k, sinon risque qu'on tombe sur n, qui existe déjà dans ce code.
// (Ou alors remplacer n par m, puis randomiser le nom de variable de l'indice k ?)
```

+++

```{code-cell} c++
---
tags: [hide-output]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
int n, r;
n = N0;
r = 1;

for ( int k = 1; k <= n; k++ ) {
    r = r * k;
}
```

+++

Assigner la valeur attendue de r à la variable result
```{code-cell} c++
---
editable: true
tags: [answer]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
int result;
```

+++

```{code-cell} c++
---
editable: true
tags: [answer]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
cin >> result
```

+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: true}
---
CHECK( result == r );
```
