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

### Objectif pédagogique : échange de variable correct

```{code-cell} c++
---
editable: false
tags: [hide-cell]
---

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
CONST I1 = RANDOM_INT(0, 7);
I1
```

+++

```{code-cell} c++
---
tags: [hide-cell, variable]
---
CONST I2 = RANDOM_INT(8, 15);
I2
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
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
    Y
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
