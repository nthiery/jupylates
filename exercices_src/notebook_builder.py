import os, copy, random, re, glob
import nbformat as nbf
import jupytext    # type: ignore

STRING_QUOTE = '"'
VECTOR_OPEN="{"
VECTOR_CLOSE="}"
PL_COMMENT="///"

NB_JUPYTEXT= {"text_representation": {
                               "extension": ".md",
                               "format_name": "myst"}}

PY_KERNELSPEC= {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
}

CPP_KERNELSPEC= {
      "display_name": "C++17",
      "language": "C++17",
      "name": "xcpp17"
}

SOLUTION_METADATA= {
      "editable": "true",
      "nbgrader": {
          "grade": "false",
          "grade_id": "init",
          "locked": "false",
          "schema_version": "3",
          "solution": "true"
       }
}

HIDDEN_METADATA= {
       "editable": "false",
       "tags": ['hide-cell']
}

CHECK_METADATA= {
       "editable": "false",
       "nbgrader": {
           "grade": "true",
           "grade_id": "check",
           "locked": "true",
           "points": "1",
           "schema_version": "3",
           "solution": "false"
       },
       "tags": ['hide-cell']
}

def write_nb(cells, language, outfile):
    metadata = dict(jupytext=NB_JUPYTEXT)
    if language == "python":
        metadata.update({"kernelspec" : PY_KERNELSPEC})
    if language == "cpp":
        metadata.update({"kernelspec" : CPP_KERNELSPEC})
    meta = nbf.from_dict(metadata)
    notebook = nbf.v4.new_notebook(metadata=meta, cells=cells)
    jupytext.write(notebook, outfile, fmt="md:myst")


def find_objectif(code):
    for (line_nb, line) in enumerate(code.splitlines()):
        if 'Objectif Pédagogique' in line or 'Objectif pédagogique' in line:
            return line
    return None


def split_cells(code):
    begin = re.compile(r'\s*' + PL_COMMENT + ' (BEGIN) (\w+)')

    items = []
    objectif = find_objectif(code)
    if objectif is not None:
        items.append(nbf.v4.new_markdown_cell(source=objectif.replace('///', '###'), metadata={}))
    item = {'source': '', 'metadata': {}}

    for (line_nb, line) in enumerate(code.splitlines()):
        match = begin.match(line)

        if 'randomization.h' in line:
            line = line.replace('randomization.h', 'jupyter_exercizer_helpers.hpp')

        if match or "main()" in line:
            items.append(nbf.v4.new_code_cell(source=item['source'], metadata=item['metadata']))
            item = {'source': '', 'metadata': {}}
        if "main()" in line:
            continue
        if 'BEGIN HIDDEN' in line:
            item['metadata'].update(HIDDEN_METADATA)
        if 'BEGIN SOLUTION' in line:
            item['metadata'].update(SOLUTION_METADATA)
        if 'CHECK' in line:
            item['metadata'].update(CHECK_METADATA)
        item['source'] += f'{line}\n'
        if 'END HIDDEN' in line:
            items.append(nbf.v4.new_code_cell(source=item['source'], metadata=item['metadata']))
            item = {'source': '', 'metadata': {}}

    items.append(nbf.v4.new_code_cell(source=item['source'], metadata=item['metadata']))
    items.append(nbf.v4.new_markdown_cell(
        source=":::{admonition} Consigne\n\nQuelle est la valeur attendue de r?\n\n:::"))

    return items


for filename in glob.glob("/home/cmarmo/software/cpp-info111/exercices_src/*/*.cpp"):
    dir_name = filename.split("/")[-2]
    outfile = dir_name + "/cpp_" + filename.split("/")[-1].replace(".cpp", ".md")
    if os.path.isfile(filename) and os.path.isdir(dir_name):
        f = open(filename, "r")
        code = f.read()
    else:
        continue

    items = split_cells(code)
    write_nb(items, "cpp", outfile)
