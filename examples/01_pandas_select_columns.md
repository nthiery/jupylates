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
---

```{code-cell} ipython3
:tags: [hide-cell]

from random import randint
import numpy as np
import pandas as pd

NROWS = randint(2, 5)
NCOLUMNS = randint(10, 12)
columnnames = [f"C{randint(0, NCOLUMNS-1)}"
            for i in range(randint(2, min(3, NCOLUMNS)))]

T = pd.DataFrame(
    data=np.array(range(NROWS*NCOLUMNS)).reshape(NROWS, NCOLUMNS),
    columns=[f"C{str(col)}" for col in range(NCOLUMNS)],
    index=[f"L{str(line)}" for line in range(NROWS)])
```

+++ {"tags": []}

:::{admonition} Instructions

Let `T` be the following Pandas DataFrame with {eval}`NROWS` rows and {eval}`NCOLUMNS` columns:

{eval}`T`

Extract the columns {eval}`columnnames` from `T`, in the given order.

:::

```{code-cell} ipython3
:tags: [hide-cell]

SOLUTION = T[columnnames]
```

```{code-cell} ipython3
:tags: [solution]

SOLUTION
```

```{code-cell} ipython3
:tags: [hide-cell, test]

answer = _
assert type(answer) == type(SOLUTION)
pd.testing.assert_frame_equal(answer, SOLUTION)
```
