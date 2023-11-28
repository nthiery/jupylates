---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.2
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

### Objectif pédagogique : différence entre accumulateur et simple affectation

```{code-cell}
:editable: false
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;

CONST I1 = RANDOM_INT(5, 17);
```

```{code-cell}
int x, y;
x = 0;
y = 0;
while ( x < I1 ) {
    x = x + 1;
    y = 1;
}
```

:::{admonition} Consigne

Quelle est la valeur attendue de x et y?

:::

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
int resultx = INPUT(
    /// BEGIN SOLUTION
    I1
    /// END SOLUTION
);
```

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
int resulty = INPUT(
    /// BEGIN SOLUTION
    1
    /// END SOLUTION
);
```

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
CHECK( resultx == x );
CHECK( resulty == y );
```
