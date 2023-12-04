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

### Objectif pédagogique: savoir faire des conditionnelles filées et imbriquées propres

```{code-cell}
:editable: 'false'
:tags: [hide-cell]

#include <iostream>
#include "jupyter_exercizer_helpers.hpp"
using namespace std;
```

:::{admonition} Consigne

Au musée de Marly, les tarifs d'entrée sont définis ainsi :
Gratuit pour les enfants d'au plus 6 ans.
Tarif réduit (3 euros) pour les enfants entre 7 et 12 ans et
pour les personnes agées à partir de 65 ans.
Tarif plein (5 euros) pour les autres.
De plus, les habitants de la ville de Marly ont une réduction de 1 euro.

Compléter la fonction ci-dessous.
:::

```{code-cell}
:editable: 'false'

/** Tarif du musée de Marly
 *  @param age : l'âge du visiteur (entier)
 *  @param marly un booléen qui vaut true si le visiteur habite à Marly
 *  @return le prix à payer pour le visiteur
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
int tarif(int age, bool marly) {
    int prix;
/// BEGIN SOLUTION
    if (0 <= age and age < 7) {
        prix = 0;
    } else {
        if (12 < age and age < 65)
            prix = 5;
        else
            prix = 3;
        if (marly)
            prix = prix - 1;
    }
/// END SOLUTION
    return prix;
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
CHECK( tarif(5,true) == 0 ) ;
CHECK( tarif(5,false) == 0 );
CHECK( tarif(11,true) == 2 );
CHECK( tarif(11,false) == 3 );
CHECK( tarif(66,true) == 2 );
CHECK( tarif(66,false) == 3 );
CHECK( tarif(20,true) == 4 );
CHECK( tarif(20,false) == 5 );
```