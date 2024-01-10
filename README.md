# JuPylates

JuPylates is an exerciser engine for learning and evaluation...

## Why JuPylates

- integrates in the users's environment (for Jupyter-based courses)
- easy to deploy (at least for training purposes)
- easy to extend
  writing an exercise is (almost) no harder than writing a Jupyter notebook
- harness the full power of Jupyter and the underlying open source scientific computing ecosystem
    - rich authoring, computational (and visualization?) tools
    - multilanguage
- lean (1k lines of code), modular, interoperable
- flexible learning record managment: can e.g. be used purely locally

### Demos

A demo is accessible [here](jupylates_demo.md).

### Build an exerciser website

The repository can be built as an interactive website using
[MyST](https://mystmd.org/) and [thebe](https://thebe.readthedocs.io/en/stable/),
following those [instructions](https://mystmd.org/guide/integrating-jupyter).

Once [MyST installed](https://mystmd.org/guide/quickstart) the site can be built
running
```
myst
```
it will then be available at `http://localhost:3000`.

The site is configured in `myst.yml` to connect to a local jupyter lab
launched via
```
jupyter lab --NotebookApp.token=test-secret --NotebookApp.allow_origin='*'
```
