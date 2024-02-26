## Build an exerciser website

### With MyST

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

### With JupyterLite

TBD
