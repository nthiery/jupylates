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

Assigner la valeur attendue de r à la variable result

:::

```{code-cell} c++
---
editable: true
---
string result;
```

+++

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
// BEGIN SOLUTION
// Votre solution ici
result = NAMEstr;
// END SOLUTION
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
