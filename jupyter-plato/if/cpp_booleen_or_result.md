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

### Objectif pédagogique: opération "or"

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;

CONST I1 = RANDOM_INT(-1, 4);
```

```{code-cell}
int x = I1;
string r;
if ( x < 0 or x > 2 ) {
    r = "oui";
} else {
    r = "non";
}
```

:::{admonition} Consigne

Quelle est la valeur attendue de `r`?

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
string result = INPUT(
    /// BEGIN SOLUTION
    r
    /// END SOLUTION
);
```

+++

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
CHECK( result == r );
```