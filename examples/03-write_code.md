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
learning_objective: 'write for loops with accumulator'
---

```{code-cell}
:tags: [hide-cell, substitutions]

import random
from jupylates.jupylates_helpers import SUBSTITUTE

I1 = random.randint(1, 6)
I2 = random.randint(10, 12)

SUBSTITUTE(I1=I1, I2=I2)
```

:::{admonition} Instructions

Write code to compute the product of the integers from I1 to I2, and
store the result in a variable `p`.

:::

```{code-cell}
:tags: [answer]

p = 1;
for i in range(I1, I2+1):
    p = p * i
```

```{code-cell}
:tags: [test, hide-cell]

# TODO: enrich the model to not need that duplication
result = 1;
for i in range(I1, I2+1):
    result = result * i

assert result == p
```
