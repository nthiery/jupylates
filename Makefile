BUILDDIR=_build

clean:
	rm -rf $(BUILDDIR) jupylates_demo.ipynb

lite:
	jupytext jupylates_demo.md --to ipynb
	jupyter lite build --contents=jupylates_demo.ipynb --output-dir=$(BUILDDIR)

