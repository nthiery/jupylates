BUILDDIR=_output
CONTENTDIR=_contents

clean:
	rm -rf $(BUILDDIR) $(CONTENTDIR)

contents:
	mkdir -p $(CONTENTDIR)
	cp -rL examples $(CONTENTDIR)
	sed -i 's/"python3"/"xeus-python"/' jupylates_demo.md
	sed -i 's/"Python 3 .ipykernel."/"Python (XPython)"/' jupylates_demo.md
	jupytext jupylates_demo.md --to ipynb
	mv jupylates_demo.ipynb $(CONTENTDIR)

lite:	contents
	jupyter lite build --XeusAddon.environment_file jupyterlite-environment.yml --contents $(CONTENTDIR) --output-dir $(BUILDDIR)
