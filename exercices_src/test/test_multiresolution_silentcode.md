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
// Objective: test programs with two input zones
#include <iostream>
#include "../randomization.h"
using namespace std;
```

+++

```{code-cell} c++
---
nbgrader: {grade: false, grade_id: init, schema_version: 3,locked: false, solution: false}
---
int x;
```

+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: solution1, schema_version: 3, locked: true, solution: true}
---
/// BEGIN SOLUTION
x = 1;
/// END SOLUTION
```
+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check1, schema_version: 3, locked: true, solution: false}
---
CHECK(x == 1);
```
+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: false, grade_id: solution2, schema_version: 3, locked: true, solution: true}
---
    /// BEGIN SOLUTION
    x = 2;
    /// END SOLUTION
```
+++

```{code-cell} c++
---
editable: false
tags: [hide-cell]
nbgrader: {grade: true, points: 1, grade_id: check2, schema_version: 3, locked: true, solution: false}
---
CHECK(x == 2);
```

