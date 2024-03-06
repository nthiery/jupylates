BUILDDIR=_output

clean:
	rm -rf $(BUILDDIR) jupylates_demo.ipynb

lite:
	sed -i 's/"python3"/"xeus-python"/' jupylates_demo.md
	sed -i 's/"Python 3 .ipykernel."/"Python (XPython)"/' jupylates_demo.md
	jupytext jupylates_demo.md --to ipynb
	jupyter lite build --XeusPythonEnv.environment_file=jupyterlite-environment.yml --contents=jupylates_demo.ipynb --output-dir=$(BUILDDIR)

