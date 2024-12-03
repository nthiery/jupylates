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
learning:
  objectives:
    apply: extract a series from a dataframe
  prerequisites:
    understand: dataframe
---

+++ {"tags": ["instructors"]}

:::{hint} About this demo
:class: dropdown

This exercise illustrates:
- the use of MyST for rich text, including admonitions and embedded values
- the use of arbitrary features of the underlying language and
  libraries to generate random values (here a Pandas DataFrame) and
  test them.
- specifying learning objectives as a narrative
- the rich display of values
- one approach to structure the solution and answer enabling testing
  and displaying the solution

:::

:::{admonition} Learning objective
Extract multiple columns from a Pandas DataFrame.
:::

```{code-cell}
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

:::{admonition} Instructions
Let `T` be the following Pandas DataFrame:

{eval}`T`

Extract the columns {eval}`columnnames` from `T`, in the given order.
:::

```{code-cell}
:tags: [answer, solution, test]

from jupylates.jupylates_helpers import INPUT_EXPR
solution, answer = INPUT_EXPR("", T[COLUMN])

assert type(answer) == type(solution)
pd.testing.assert_series_equal(answer, solution)
```
