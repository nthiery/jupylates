BUILDDIR=_output
CONTENTDIR=_contents

clean:
	rm -rf $(BUILDDIR) $(CONTENTDIR)

contents:
	mkdir -p $(CONTENTDIR)
	cp jupylates_demo.md $(CONTENTDIR)
	cp -r examples $(CONTENTDIR)
	cd $(CONTENTDIR)
	sed -i 's/"python3"/"xeus-python"/' jupylates_demo.md
	sed -i 's/"Python 3 .ipykernel."/"Python (XPython)"/' jupylates_demo.md
	jupytext jupylates_demo.md --to ipynb
	

lite:	contents
	jupyter lite build --XeusPythonEnv.environment_file=jupyterlite-environment.yml --contents=$(CONTENTDIR) --output-dir=$(BUILDDIR)

