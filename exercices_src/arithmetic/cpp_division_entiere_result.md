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

### Objectif pédagogique : division entière

```{code-cell}
:editable: false
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

+++

```{code-cell}
:tags: [hide-cell, variable]

CONST I1 = RANDOM_CHOICE(3, 5, 7);
I1
```

+++

```{code-cell}
:tags: [hide-cell, variable]

CONST I3 = RANDOM_CHOICE(1, 2, 4, 8, 11, 13, 16, 17, 19, 22);
I3
```

+++

```{code-cell}
:tags: [hide-output, substitution]

int r;
r = I3 / I1;
```
+++

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
int result = INPUT(
    /// BEGIN SOLUTION
    I3 / I1
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
