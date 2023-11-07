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

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---
#include<iostream>
#include "randomization.h"

CONST C = RANDOM_INT(-2, 2);
```

+++

```{code-cell} c++
---
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
int I;
// Initialiser la variable I à la valeur C
```

+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: solution, schema_version: 3, locked: true, solution: true}
---
/// BEGIN SOLUTION
I = C;
/// END SOLUTION
```
+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check, schema_version: 3, locked: true, solution: false}
---
CHECK( I == C );
```

