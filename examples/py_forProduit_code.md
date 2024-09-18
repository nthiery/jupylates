---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
learning_objective: 'boucle for avec accumulateur'
---

```{code-cell}
:tags: [hide-cell, substitutions]

import random
from jupylates.jupylates_helpers import SUBSTITUTE

I1 = random.randint(1, 6)
I2 = random.randint(10, 12)

SUBSTITUTE(I1=I1, I2=I2)
```

:::{admonition} Consigne

Écrivez le code permettant de mettre dans la variable `p` le produit
des entiers compris entre I1 et I2 inclus.

:::

```{code-cell}
:tags: [solution]

p = 1;
for i in range(I1, I2+1):
    p = p * i
```

```{code-cell}
:tags: [test, hide-cell]

result = 1;
for i in range(I1, I2+1):
    result = result * i
assert result == p
```
