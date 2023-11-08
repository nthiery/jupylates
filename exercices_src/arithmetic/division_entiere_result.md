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

### Objectif Pédagogique : division entière.

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---

#include <iostream>
#include "../randomization.h"
using namespace std;

CONST I1 = RANDOM_CHOICE(3, 5, 7);
CONST I3 = RANDOM_CHOICE(1, 2, 4, 8, 11, 13, 16, 17, 19, 22);

```

+++

```{code-cell} c++
---
tags: [hide-output]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

int r;
r = I3 / I1;
/// Assigner la valeur attendue de r à la variable result
int result;
cin >> result;
```

+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: false}
---
CHECK( result == r );
```
