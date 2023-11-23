import copy, random, re, glob
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

def split_cells(code):
    begin = re.compile(r'\s*' + PL_COMMENT + ' (BEGIN) (\w+)')

    items = []
    items.append(nbf.v4.new_markdown_cell(source="### Objectif Pédagogique :", metadata={}))
    items.append(nbf.v4.new_markdown_cell(source=":::{admonition} Consigne\n\nConsigne generique\n\n:::"))
    item = {'source': '', 'metadata': {}}

    for (line_nb, line) in enumerate(code.splitlines()):
        match = begin.match(line)

        if 'randomization.h' in line:
            line = line.replace('randomization.h', 'jupyter_exercizer_helpers.hpp')

        if line == "int main() {":
            continue
        if line == "    return 0;":
            continue
        if line == "}":
            continue

        if 'HIDDEN' in line:
            item['metadata'].update(HIDDEN_METADATA)
        if 'SOLUTION' in line:
            item['metadata'].update(SOLUTION_METADATA)
        if 'CHECK' in line:
            item['metadata'].update(CHECK_METADATA)
        if line == "" or match:
            items.append(nbf.v4.new_code_cell(source=item['source'], metadata=item['metadata']))
            item = {'source': '', 'metadata': {}}
        item['source'] += f'{line}\n'

    items.append(nbf.v4.new_code_cell(source=item['source'], metadata=item['metadata']))

    return items


for filename in glob.glob("/home/cmarmo/software/cpp-info111/exercices_src/pointeurs/*.cpp"):
    outfile = "pointeurs/cpp_" + filename.split("/")[-1].replace(".cpp", ".md")
    f = open(filename, "r")
    code = f.read()

    items = split_cells(code)
    write_nb(items, "cpp", outfile)
