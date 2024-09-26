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
learning_objective: 'déclarer une variable'
---

```{code-cell} ipython3
:tags: [hide-cell]

from random import randint
I1 = randint(1,10)
```

:::{admonition} Consigne

Déclarez une variable entière `R` et affectez lui la valeur {eval}`I1`.

:::

```{code-cell} ipython3
:tags: [answer]

R = I1
```

```{code-cell} ipython3
:tags: [test, hide-cell]

assert R == I1
```
