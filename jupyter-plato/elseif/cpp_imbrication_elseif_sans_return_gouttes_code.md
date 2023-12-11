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

On considère un médicament dont la prescription a les règles suivantes:
Le traitement court a une durée inférieure à 7 jours et
le traitement long une durée supérieure à 8 jours.
Pour un enfant de moins de 2 ans, il faut 10 gouttes par jour pour le traitement court,
et 5 gouttes par jour pour le traitement long.
Pour un enfant de 2 à 16 ans, 13 gouttes par jour pour le traitement court,
et 7 gouttes par jour pour le traitement long.
A partir de 16 ans, 15 gouttes par jour pour le traitement court,
et 9 gouttes par jour pour le traitement long.

Compléter la fonction ci-dessous.

:::

```{code-cell}
:editable: 'false'

/** Nombre total de gouttes à prescrire sur l'ensemble du traitement
 *  @param age : l'âge du patient
 *  @param duree : durée du traitement
 *  @return le nombre total de gouttes sur l'ensemble du traitement
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
int nombreTotalGouttes(int age, int duree) {
    int nbTotal;
/// BEGIN SOLUTION
    if (duree <= 7)
        if (age < 2)
            nbTotal = 10*duree;
        else if (age < 16)
            nbTotal = 13*duree;
        else
            nbTotal = 15*duree;
    else
        if (age < 2)
            nbTotal = 5*duree;
        else if (age < 16)
            nbTotal = 7*duree;
        else
            nbTotal = 9*duree;
/// END SOLUTION
    return nbTotal;
}
```

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
CHECK( nombreTotalGouttes(1,2) == 20 ) ;
CHECK( nombreTotalGouttes(1,10) == 50 );
CHECK( nombreTotalGouttes(11,2) == 26 );
CHECK( nombreTotalGouttes(11,10) == 70 );
CHECK( nombreTotalGouttes(20,3) == 45 );
CHECK( nombreTotalGouttes(20,10) == 90 );
```