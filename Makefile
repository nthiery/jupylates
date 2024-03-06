BUILDDIR=_output

clean:
	rm -rf $(BUILDDIR) jupylates_demo.ipynb

contents:
	mkdir -p $(BUILDDIR)/contents
	cp jupylates_demo.md $(BUILDDIR)/contents
	cp -r examples $(BUILDDIR)/contents
	cd $(BUILDDIR)/contents
	sed -i 's/"python3"/"xeus-python"/' jupylates_demo.md
	sed -i 's/"Python 3 .ipykernel."/"Python (XPython)"/' jupylates_demo.md
	jupytext jupylates_demo.md --to ipynb
	

lite:	contents
	jupyter lite build --XeusPythonEnv.environment_file=jupyterlite-environment.yml --contents=$(BUILDDIR)/contents --output-dir=$(BUILDDIR)

