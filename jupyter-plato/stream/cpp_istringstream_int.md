---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

# Objectif pédagogique : lire depuis une chaîne de caractères avec un flux

```{code-cell}
:tags: [hide-cell]

#include <iostream>
#include <sstream>
using namespace std;
CONST I1 = RANDOM_INT(1,10);
CONST I2 = RANDOM_INT(1,10);
CONST I3 = RANDOM_INT(1,10);
CONST I4 = RANDOM_INT(1,10);
```

+++

:::{admonition} Consigne

Quelle est la valeur de `K` à la fin de l'exécution du code suivant?

:::

```{code-cell}
istringstream flux("I1 I2 I3 I4");
int I, J, K;

flux >> I >> J >> K;
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
int r = INPUT(K);
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
CHECK( r == K );
```
