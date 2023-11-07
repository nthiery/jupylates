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
using namespace std;

CONST C1 = RANDOM_INT(-2, 2);
```

+++

```{code-cell} c++
---
editable: false
nbgrader: {grade: false, grade_id: output, schema_version: 3,locked: false, solution: false}
---
int X = C1;
cout << X << endl;
```


