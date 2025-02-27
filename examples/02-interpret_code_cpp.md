---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: C++17
  language: C++17
  name: xcpp17
---

+++ {"tags": ["instructors"]}

:::{hint} About this demo
:class: dropdown

This exercise illustrates:
- an exercise in C++
- substitutions of random literals in C++
- requesting an integer as answer
:::

```{code-cell}
:tags: [substitutions, hide-cell]

#include <jupylates_helpers.hpp>

int I1 = RANDOM_INT(1,  7); SUBSTITUTE_VARIABLE(I1);
int I2 = RANDOM_INT(8, 15); SUBSTITUTE_VARIABLE(I2);
```

:::{admonition} Instructions
What's the value of `r` after executing the following code?
:::

```{code-cell}
int X = I1;
int Y = I2;

int Z;

Z = X;
X = Y;
Y = Z;
int r = Y;
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

int answer, solution;
INPUT_INT("r", solution, answer, r);

CHECK(answer == solution)
```
