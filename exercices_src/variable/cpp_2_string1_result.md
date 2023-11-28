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

### Objectif pédagogique : comprendre la difference entre valeur et nom d'une variable de type string

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
CONST NAMEstr = RANDOM_CHOICE("Bob", "Barbara", "Pierre", "Paul", "Jeanne", "Camille");
NAMEstr
```

+++

```{code-cell} c++
---
tags: [hide-output, substitution]
---

string NAME = NAMEstr;
string r = NAME;
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
string result = INPUT(
    /// BEGIN SOLUTION
    NAMEstr
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
