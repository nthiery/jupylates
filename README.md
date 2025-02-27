---
jupytext:
  cell_metadata_filter: all,-autoscroll,-collapsed,-scrolled,-trusted,-ExecuteTime,-jp-MarkdownHeadingCollapsed,-editable,-deletable
  notebook_metadata_filter: kernelspec,jupytext,exports,math,rise,semantic,-jupytext.text_representation.jupytext_version
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# JuPylates

JuPylates is an exerciser engine for training (and evaluation)

## Why JuPylates

- harness the full power of Jupyter and the underlying open source
  scientific computing ecosystem
    - rich authoring, computational (and visualization?) tools
    - multilanguage
- integrates in the users's environment and course material (for Jupyter-based courses)
- writing an exercise is (almost) no harder than writing a Jupyter notebook
- easy to deploy (at least for training purposes)
- easy to extend
- lean (1k lines of code), modular, interoperable
- flexible privacy friendly learning record managment: can e.g. be used purely locally

## Status and limitations

Jupylates is still a prototype with pieces subject to changes without
prior notice. Nevertheless, it's used in production in a few classes
at Université Paris-Saclay, and early adoption and feedback is most
welcome.


Future evolutions:
- support interactive widgets
- support interactive MyST features such as `eval` (it is currently
  emulated).
- Improve the execution model to reduce the current need for
  duplication for certain types of exercices.
- Play back previous student attempts by recording the random seed and
  student's input.
- Support more programming languages
- Support multistep exercises

## Installation

```
pip install git+https://github.com/nthiery/jupylates.git   # ⚠️ subject to change ⚠️
```

## Getting started

This runs Jupylates on all the exercises in the `examples` directory:

```{code-cell}
from glob import glob
from jupylates import Exerciser
Exerciser(glob("examples/*.md"), mode="debug")  # choose from debug, train, exam
```

## Documentation

### Authoring exercises

A Jupylates exercise is a Jupyter notebook annotated with some
metadata (mostly cell tags) to specify the role of each cell together
with some annotations in the code to delineate solutions and answer
zones. Based on these, Jupylates will render and execute the notebook
in a controlled way (called *execution model*). Generally speaking,
the cells of the notebook will be executed and rendered in order until
reaching the first answer cell. After the user's answer, the remaining
cells will be executed to validate the answer, provide feedback, etc.

The Jupyter notebook can be authored in the classical `ipynb` format
or alternatively (our recommendation) in Markdown (e.g. Jupytext's
MyST-Markdown format).

<div class="alert alert-info">

Some of the features of Jupylate's execution model require a few
helper functions implemented in the language of the notebook. For now,
there are helper functions implemented in Python and C++, and
typically provided as a small library. That library may provide
additional helpers to help with randomizing exercises in this
language. Other than that, Jupylates is language agnostic.

</div>

<div class="alert alert-info">

The execution model will feel familiar to users of nbgrader, up to
using cell tags rather than the more verbose nbgrader metadata. The
main motivation is to make it easier to edit exercises directly in
Markdown. nbgrader metadata is actually supported as an alternative,
and reciprocally we plan to contribute to nbgrader support for similar
lightweight annotations.

</div>

<div class="alert alert-primary">

Before and while diving into the details, we recommend to explore the
provided examples (see above) and read their source notebook and their
*About* comments; they will guide you through the main features of
Jupylates.

</div>

Here is a complete description of how the Jupylates execution model
treats cells (more than one item may apply):

-   *Instructor cell* (markdown cell with an `instructors` tag): the
    cell is hidden, except in debug mode.  
    Typical use case: provide context information for authors, such as
    learning objectives, things to do, or credits

-   *Hidden cell* (code cell with a tag `hide-cell`, `hide-input` or
    `hide-output` respectively): the cell, its output
    or its content respectively, is hidden.  
    Typical use case: hide boiler plate code or randomization that the
    user needs not see or should not see.

-   *Substitution cell* (code cell with a `substitution` tag): if the
    cell outputs a JSON line of the form `{source: target}`, then the
    source string is substituted by the target string whenever it
    appears as a standalone word in a subsequent cell. The cell may
    output several such lines.
	
	The Jupylates utilities for the language can typically provide
    helpers to easily define such substitutions. This is typically
    used for randomizing simple literal values or chunks of code in
    the exercise. Here we show how to substitute a word by an
    arbitrary string:
	``` python
	from jupylate_helpers import SUBSTITUTE
	SUBSTITUTE(FOO="BAR")
	```
	and in C++:
	``` c++
	#include <jupylate_helpers.hpp>
	SUBSTITUTE("FOO", "BAR");
	```

    Here we substitute a variable name by its current value in Python:
	``` python
	from jupylate_helpers import SUBSTITUTE
	X1 = 13
	SUBSTITUTE(X1=X1)
	```
	and in C++:
	``` c++
	#include <jupylate_helpers.hpp>
	int X = 13; 
	SUBSTITUTE_VARIABLE(X);
	```

-   *Answer cell* (code cell with an `answer` tag): the cell specifies
    how to request answers from the user. To catter for a variety of
    use cases, there can be several alternatives:
    -   Case 1: the cell also has the tag `solution`.
        -   Case 1.1: the cell contains one or many call(s) of the
            form `INPUT_XXX("label", ..., solution)`, where XXX is one
            of `INT`, `TEXT`, `EXPR`, `BOOL`. Then a UI will be
            displayed with the given label to input a value. Upon
            validation, the above code will be replaced by
            `INPUT_XXX("label", ..., solution, user's answer)`, to be
            interpreted by the Jupylates utilities in the given kernel.  
		    Examples:
            ```c++
            int answer;
            int solution;
            INPUT_INT("r", solution, answer, r)
            ```
            ```python
            solution, answer = INPUT_INT("r", r)
            ```

            In both examples above, the solution and answer will be
			stored in the `solution` and `answer` variables
			respectively when running the notebook in Jupylates, and
			the solution will be stored in both variables when running
			the notebook normally. This makes it easy to write tests
			by comparing the value of `solution` and `answer`.

        -   Case 1.2: The cell contains solution delimiters:
            ```
            bla bla
            ### BEGIN SOLUTION
            asdfasdf
            ### END SOLUTION
            asdfasdf
            ### BEGIN SOLUTION
            ...
            ### END SOLUTION
            ```
            Then the cell is displayed with each solution zone replaced by an input zone.  
            One can use an other prefix for the delimiters than `###`; e.g. `///` for C++.  

            To be experimented with: duplicate the cell in the
            executed notebook, so that the first cell evaluates the
            user's answer, and the second cell the solution, to enable
            comparing them.

       -   Case 1.3: Same as 1.2, with implicit `BEGIN SOLUTION` and
           `END SOLUTION` at the beginning and end of the cell.
        
    -   Case 2: otherwise, a textarea is displayed for the user to
        input the answer, initialized with the content of the cell

    Current limitation: at this stage, there can be no more than a
    single answer cell.


-   *Solution cell* (code cell with a `solution` tag): eventually,
    Jupylates will be able to extract the solution from that cell; see
    also `answer` above.

-   *Test cell* (code cell with a `test` tag): a user attempt at the
    exercise is successful if and only if the execution of that cell
    raises no error. There may be several test cells, in which case
    none should raise an error.

### Learning record and recommender

TODO

<!--
### Demos

A demo is accessible [here](https://jupyter.gitlab.dsi.universite-paris-saclay.fr/jupylates/lab/index.html?path=jupylates_demo.ipynb).
-->
