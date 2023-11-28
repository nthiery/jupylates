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

```

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

/// BEGIN HIDDEN
/// Objectif pédagogique: écrire des tests simples

#include "jupyter_exercizer_helpers.hpp"
/// END HIDDEN
```

```{code-cell}

/* On suppose que vous disposez de la fonction dont l'en-tête est donné
   ci-dessous (vous ne devez donc pas écrire de code pour cette fonction) */
int F(int X);

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
/// BEGIN HIDDEN

// CHECK doit être redéfinie pour ne pas afficher l'expression ni la ligne
#undef CHECK
#define CHECK(test) if (!(test)) std::cout << "Test failed in file " << __FILE__ \
				            << std::endl

// La fonction F sera appelée par le test de l'étudiant sur une seule
// valeur V. Aussi, pour vérifier que le test est correct, on va
// introduire un contexte et lancer le test de l'étudiant plusieurs
// fois en faisant varier ce contexte.

int contexte;
int F(int X) {
    return X - contexte;
}

CONST V = RANDOM_INT(-2, 2);
CONST T = RANDOM_INT(-2, 2);

```

```{code-cell}
    for ( contexte = -10; contexte < 10; contexte ++ ) {
        std::cout << "V: " << V << ", contexte: " << contexte << std::endl;
        /// END HIDDEN
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
        /* En utilisant la fonction CHECK, écrire un test vérifiant
         * que F(V) est égal à T (une seule ligne de code).
         */
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
        /// BEGIN SOLUTION
        CHECK( F(V) == T );
        /// END SOLUTION
```

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

        /// BEGIN HIDDEN
    }
}
/// END HIDDEN
```

```{code-cell}

```

:::{admonition} Consigne

Quelle est la valeur attendue de r?

:::
