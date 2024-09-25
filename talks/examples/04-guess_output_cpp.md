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

```{code-cell}
:tags: [hide-cell]

#include <sstream>
#include "jupylates_helpers.hpp"
using namespace std;

CONST I1 = RANDOM_INT(0, 6);
CONST I2 = I1 + RANDOM_INT(1, 4);

ostringstream cout;
```

:::{admonition} Instructions

What's the output of the following code?

:::

:::{tip}
:class: dropdown
Spell your answer in the form `"83152"`.
:::

```{code-cell}
for (int I = I1; I <= I2 ; I = I + 1 ) {
    cout << I;
}
```

```{code-cell}
:tags: [hide-cell]

string SOLUTION = cout.str();
```

```{code-cell}
:tags: [solution]

string _ = INPUT(
    /// BEGIN SOLUTION
    SOLUTION
	/// END SOLUTION
);
```

```{code-cell}
:tags: [test, hide-cell]

CHECK( _ == SOLUTION );
```
