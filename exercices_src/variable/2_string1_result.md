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

### Objectif Pédagogique : comprendre la difference entre valeur et nom d'une variable de type string.

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: header, schema_version: 3, locked: true, solution: false}
---

#include <iostream>
#include "randomization.h"

using namespace std;

CONST NAMEstr = RANDOM_CHOICE("Bob", "Barbara", "Pierre", "Paul", "Jeanne", "Camille");

```

+++

```{code-cell} c++
---
tags: [hide-output]
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---

string NAME = NAMEstr;
string r = NAME;
```

+++

Assigner la valeur attendue de r à la variable result
```{code-cell} c++
---
editable: true
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
string result;
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
