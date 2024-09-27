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

## Usage

This runs Jupylates on all exercises in the `examples` directory:

```
from glob import glob
from jupylates import Exerciser
Exerciser(glob("examples/*.md"), mode="debug")  # choose from debug, train, exam
```

## Documentation

None at this stage, sorry. Look at the examples and at the
[notebook](talks/2024-09-25-PyData.md) of the PyData Paris-2024's talk.

<!--
### Demos

A demo is accessible [here](https://jupyter.gitlab.dsi.universite-paris-saclay.fr/jupylates/lab/index.html?path=jupylates_demo.ipynb).
-->
