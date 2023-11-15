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
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---

#include <iostream>
#include "randomization.h"
using namespace std;
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
CONST I1 = RANDOM_INT(3, 9);
I1
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
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

Assigner la valeur attendue de r à la variable result
```{code-cell} c++
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
bool result;
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
