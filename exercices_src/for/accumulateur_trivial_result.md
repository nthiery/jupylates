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
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
#include <iostream>
#include "randomization.h"
using namespace std;

#define CHECK(C) if ( !(C) ) { throw std::runtime_error(\"\\x1b[48;5;224mTest failed: \"#C); }

CONST RINIT = RANDOM_INT(1, 7);
CONST IMAX = RANDOM_INT(2, 4);

```

+++

```{code-cell} c++
---
tags: [hide-output]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
int r = RINIT;
for ( int I = 1; I <= IMAX ; I = I + 1 ) {
    r = r + I;
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
cin >> result;
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
