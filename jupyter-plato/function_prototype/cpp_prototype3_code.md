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
par `{`. Regardez les appels dans les cellules suivantes pour voir le
nom de la fonction et son utilisation.

:::

```{code-cell}
/** Compte le nombre de caractères d'une chaîne de caractères
 * @param une chaîne de caractères a
 * @return le nombre de caractères de a
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
int nbCaracteres(string a) {
/// END SOLUTION
    return a.size();
}

```

```{code-cell}
nbCaracteres("bonjour")
```

```{code-cell}
nbCaracteres("aujourd'hui")
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
CHECK( string(typeid(nbCaracteres).name()).find(string("FiNSt")) != string::npos )
CHECK( nbCaracteres("bonjour") == 7 );
CHECK( nbCaracteres("aujourd'hui") == 11 );
```
