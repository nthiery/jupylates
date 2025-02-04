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
- guessing the output of code
- requesting a text answer
- random substitutions
:::

:::{admonition} Learning objective
Understand the step by step execution of a for loop.
:::

```{code-cell}
:tags: [hide-cell]

#include <sstream>
#include <jupylates_helpers.hpp>

CONST I1 = RANDOM_INT(0, 6);
CONST I2 = I1 + RANDOM_INT(1, 4);

std::ostringstream cout;
```

:::{admonition} Instructions
What's the output of the following code?
:::

:::{tip}
:class: dropdown
Spell your answer in the form `83152`.
:::

```{code-cell}
for (int I = I1; I <= I2 ; I = I + 1 ) {
    cout << I;
}
```

```{code-cell}
:tags: [answer, solution, test, hide-output]

std::string answer, solution;
INPUT_TEXT("", solution, answer, cout.str());

CHECK(answer == solution);
```
