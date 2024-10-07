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

The execution model should still be refined, the current
implementation does not yet support widgets, MyST's eval support is
emulated, ...

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

Sorry, there is no formal documentation yet. Please read the *About* comments in the examples;
they will guide you through the main features of Jupylates.

<!--
### Demos

A demo is accessible [here](https://jupyter.gitlab.dsi.universite-paris-saclay.fr/jupylates/lab/index.html?path=jupylates_demo.ipynb).
-->
