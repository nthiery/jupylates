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

+++ {"tags": ["learning objectives"]}

:::{hint} About this demo
:class: dropdown

This exercise illustrates:
- an exercise in C++
- substitutions of random code
:::

```{code-cell}
:tags: [substitutions, hide-cell]

#include <jupylates_helpers.hpp>

SUBSTITUTE("VAL_OR_REF ", RANDOM_CHOICE("", "&"));
SUBSTITUTE("PLUS_OR_MINUS", RANDOM_CHOICE("+", "-"));
SUBSTITUTE("A", RANDOM_CHOICE("a", "b", "c"));
SUBSTITUTE("D", RANDOM_CHOICE("d", "e", "f"));
```

:::{admonition} Instructions
What's the value of `A` after executing the following code:
:::

```{code-cell}
int A = 1 PLUS_OR_MINUS 1;
int VAL_OR_REF D = A;
D = 4;
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

int answer, solution;
INPUT_INT("A", solution, answer, A);

CHECK(answer == solution);
```
