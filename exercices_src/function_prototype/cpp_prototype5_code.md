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

### Objectif pédagogique : écriture d'entête de fonction

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include <typeinfo>
#include <string>
#include "jupyter_exercizer_helpers.hpp"

using namespace std;
```

:::{admonition} Consigne

Écrivez ci-dessous l'entête de la fonction en n'oubliant pas de finir
par `{`.  Regardez les appels dans les cellules suivantes pour voir le
nom de la fonction et son utilisation.

:::

```{code-cell}

/** Affiche un compte à rebours commençant par l'entier pris en paramètre
 * @param n un entier
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
void afficheCompteARebours(int n) {
/// END SOLUTION
    for (int i=n; i>=0; i--) {
        cout << i << endl;
    }
}

```

```{code-cell}
afficheCompteARebours(5)
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
CHECK( typeid(afficheCompteARebours).name() == string("FviE") );
```
