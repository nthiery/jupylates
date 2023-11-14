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

### Objectif Pédagogique : échange de variable correct.

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---

#include <iostream>
#include "randomization.h"
using namespace std;

CONST I1 = RANDOM_INT(0, 7);
CONST I2 = RANDOM_INT(8, 15);

```

+++

```{code-cell} c++
---
tags: [hide-output]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

int X, Y, Z;
X = I1;
Y = I2;

Z = X;
X = Y;
Y = Z;
int r = Y;
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
