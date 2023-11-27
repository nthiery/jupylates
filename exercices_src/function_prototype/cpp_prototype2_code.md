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

### Objectif Pédagogique : écriture d'en-tête de fonction avec des types autres que int.

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"

using namespace std;
```

:::{admonition} Consigne

Ecrire ci-dessous l'en-tête de la fonction
en n'oubliant pas de finir par `{`.
Regarder les appels dans les cellules suivantes pour
voir le nom de la fonction et son utilisation.

:::

```{code-cell}
/** Multiplie un entier et un réel
 * @param un entier a et un réel b
 * @return le produit réel de a par b
 **/
```

```{code-cell}
---
editable: 'true'
nbgrader:
  grade: 'false'
  grade_id: init
  locked: 'false'
  schema_version: '3'
  solution: 'true'
---
/// BEGIN SOLUTION
float produit(int a, float b) {
/// END SOLUTION
    return a * b;
}

```

```{code-cell}
produit(3, 2.5)
```

```{code-cell}
produit(2, 5.4)
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
CHECK( produit(3, 2.5) == 7.5f );
CHECK( produit(2, 5.4) == 10.8f );
```