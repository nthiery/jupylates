import copy
import nbformat
import IPython  # type: ignore
from IPython.core.display_functions import display  # type: ignore
import ipywidgets  # type: ignore
from typing import List
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

answer_code = {
    "C++11": "auto result = {answer};",
    "C++14": "auto result = {answer};",
    "C++17": "auto result = {answer};",
    "python": "result = {answer}",
}

class Exercizer(ipywidgets.VBox):
    def __init__(self, exercizes: List[str]):
        self.exercizes = exercizes

        # View
        self.exercize_zone = ipywidgets.Output()
        self.answer_zone = ipywidgets.Text()
        self.run_button = ipywidgets.Button(description="Run")
        self.result_label = ipywidgets.Label()
        self.next_button = ipywidgets.Button(description="Next exercize")
        self.controler_zone = ipywidgets.HBox(
            [self.run_button, self.result_label, self.next_button]
        )

        # Controler
        self.next_button.on_click(lambda event: self.next_exercize())
        self.run_button.on_click(lambda event: self.run_exercize())

        self.set_exercize(0)
        super().__init__([self.exercize_zone, self.controler_zone])

    def next_exercize(self):
        self.set_exercize((self.current_exercize_number + 1) % len(self.exercizes))
                                  
    def set_exercize(self, i: int):
        self.current_exercize_number = i
        self.current_notebook = nbformat.read(
            self.exercizes[self.current_exercize_number], as_version=4
        )
        self.display_exercize(self.current_notebook)
        self.result_label.value = ""

    def run_exercize(self):
        success = self.run_notebook(self.current_notebook, self.answer_zone.value)
        self.result_label.value = "Bravo" if success else "Raté"
    
    def display_exercize(self, notebook):
        with self.exercize_zone:
            self.exercize_zone.clear_output(wait=True)
            for cell in notebook.cells:
                if "tags" in cell["metadata"] and "answer" in cell["metadata"]["tags"]:
                    self.answer_zone.value = ""
                    display(self.answer_zone)
                elif cell["cell_type"] == "markdown":
                    display(IPython.display.Markdown(cell["source"]))
                else:
                    if "tags" not in cell["metadata"] or "hide-cell" not in cell["metadata"]["tags"]:
                        display(IPython.display.Code(cell["source"]))
    
    def run_notebook(self, notebook, answer) -> bool:
        notebook = copy.deepcopy(notebook)
        for i in range(len(notebook.cells)):
            if "tags" in notebook.cells[i]["metadata"] and "answer" in notebook.cells[i]["metadata"]["tags"]:
                language = notebook.metadata["kernelspec"]["language"]
                code = answer_code[language].format(answer=answer)
                notebook.cells[i] = nbformat.v4.new_code_cell(code)

        ep = ExecutePreprocessor(timeout=600, allow_errors=True)
        result = ep.preprocess(notebook)
        return not any(
            cell["cell_type"] == "code"
            and cell["metadata"].get("nbgrader", {}).get("solution", False)
            and cell["outputs"]
            and cell["outputs"][0]["output_type"] == "error"
            for cell in result[0]["cells"]
        )
