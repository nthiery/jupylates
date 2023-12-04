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

# Objectif Pédagogique : écrire dans une chaîne de caractères avec un flux

```{code-cell}
:tags: [hide-cell]

#include <sstream>
using namespace std;
CONST C = RANDOM_INT(-2, 2);
```

+++

:::{admonition} Consigne

Quelle est la valeur de `S` à la fin de l'exécution du code suivant?

Indication: bien mettre les guillemets.

:::

```{code-cell}
ostringstream flux;

flux << "8 + C = " << 8 + C;
string S = flux.str();
```

```{code-cell}
---
nbgrader:
  grade: false
  grade_id: init
  locked: false
  schema_version: 3
  solution: true
---
string result = INPUT(
/// BEGIN SOLUTION
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
CHECK( result == S );
```
