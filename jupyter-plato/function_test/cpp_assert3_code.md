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

### Objectif pédagogique: écrire des tests simples

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"

using namespace std;
```

```{code-cell}
---
editable: 'false'
tags: [hide-cell]
---

// La fonction F sera appelée par le test de l'étudiant sur une seule
// valeur V. Aussi, pour vérifier que le test est correct, on va
// introduire un contexte et lancer le test de l'étudiant plusieurs
// fois en faisant varier ce contexte.

int contexte;

CONST V = RANDOM_INT(-2, 2);
CONST T = RANDOM_INT(-2, 2);

```


:::{admonition} Consigne

On suppose que vous disposez de la fonction dont l'en-tête est donné
dans la cellule suivante (vous ne devez donc pas écrire de code pour cette fonction).
En utilisant la fonction CHECK, écrire un test vérifiant que F(V) est strictement inférieur à T
(une seule ligne de code).

:::


```{code-cell}

int F(int X);
```


```{code-cell}
---
editable: 'false'
tags: [hide-cell]
---

int F(int X) {
    return X - contexte;
}
```

```{code-cell}
---
editable: 'false'
nbgrader:
  grade: 'true'
  grade_id: check
  locked: 'true'
  points: '1'
  schema_version: '3'
  solution: 'false'
tags: [hide-cell]
---
void FTest() {
/// BEGIN SOLUTION
    CHECK( F(V) < T );
/// END SOLUTION
}
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

bool success;
for ( contexte = -10; contexte < 10; contexte ++ ) {
    try {
        FTest();
        success = true;
    } catch(...) {
        success = false;
        if ( F(V) < T ) {
            throw std::runtime_error("\\x1b[48;5;224mTest failed");
        }
    }
    if (success and !(F(V) < T)) {
        throw std::runtime_error("\\x1b[48;5;224mTest failed");
    }
}
```