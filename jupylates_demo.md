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

# Why JuPylates

- integrates in the users's environment (for Jupyter-based courses)
- easy to deploy (at least for training purposes)
- easy to extend
  writing an exercise is (almost) no harder than writing a Jupyter notebook
- harness the full power of Jupyter and the underlying open source scientific computing ecosystem
    - rich authoring, computational (and visualization?) tools
    - multilanguage
- lean (1k lines of code), modular, interoperable
- flexible learning record managment: can e.g. be used purely locally

+++

# Démo

+++

L'application, en mode entraînement, sur une liste d'exercices (ici tous les exercices dans le dossier `examples`):

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
import glob
from jupylates import Exerciser
Exerciser(glob.glob("examples/*.md"), mode="train")
```
