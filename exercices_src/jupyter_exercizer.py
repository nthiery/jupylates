import copy, getpass, json, os, random, re, requests
from datetime import datetime
import IPython  # type: ignore
from IPython.core.display_functions import display  # type: ignore
import ipywidgets  # type: ignore
import nbformat
import jupytext    # type: ignore
from typing import Any, List
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

from code_randomizer import Randomizer


Notebook = Any


class ExecutionError(RuntimeError):
    pass


answer_regexp = re.compile(r"INPUT\(.*\)", re.DOTALL)


class Exercizer(ipywidgets.VBox):
    def __init__(self, exercizes: List[str]):
        # learner owner of the session
        learner = os.getenv('JUPYTERHUB_USER')
        if learner:
            self.learner = learner
        else:
            self.learner = getpass.getuser()

        self.start_time = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')

        self.exercizes = sorted(exercizes)

        #self.lrs_url = "file://" + os.getcwd() + "/.learning_record.json"
        self.lrs_url = ".learning_record.json"

        # View
        border_layout = ipywidgets.Layout(border="solid", padding="1ex")
        self.exercize_zone = ipywidgets.Output(layout=border_layout)
        self.answer_zone = [ipywidgets.Textarea()]
        self.run_button = ipywidgets.Button(
            description="Valider", button_style="primary", icon="check"
        )
        self.name_label = ipywidgets.Label()
        self.result_label = ipywidgets.Label()
        self.randomize_button = ipywidgets.Button(
            icon="dice",
            description="Variante",
            tooltip="Tire aléatoirement une autre variante du même exercice",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.next_button = ipywidgets.Button(
            icon="caret-right",
            description="Exercice suivant",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.previous_button = ipywidgets.Button(
            icon="caret-left",
            description="Exercice précédent",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.random_button = ipywidgets.Button(
            icon="dice",
            description="Exercice aléatoire",
            tooltip="Tire aléatoirement un exercice",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.controler_zone = ipywidgets.VBox(
            [
                ipywidgets.HBox(
                    [
                        self.randomize_button,
                        self.run_button,
                        self.name_label,
                        self.result_label,
                    ]
                ),
                ipywidgets.HBox(
                    [self.previous_button, self.random_button, self.next_button]
                ),
            ]
        )

        # Controler
        self.next_button.on_click(lambda event: self.next_exercize())
        self.previous_button.on_click(lambda event: self.previous_exercize())
        self.random_button.on_click(lambda event: self.random_exercize())
        self.randomize_button.on_click(lambda event: self.randomize_exercize())
        self.run_button.on_click(lambda event: self.run_exercize())

        self.set_exercize(0)
        super().__init__(
            [self.exercize_zone, self.controler_zone], layout=border_layout
        )

    def set_exercize(self, i: int):
        self.exercize_number = i
        self.exercize_name = self.exercizes[self.exercize_number]
        self.notebook = self.randomize_notebook(jupytext.read(self.exercize_name))
        self.display_exercize(self.notebook)
        language = self.notebook.metadata["kernelspec"]["language"]
        self.name_label.value = f'{self.exercize_name} ({language})'
        self.result_label.value = ""

    def next_exercize(self):
        self.set_exercize((self.exercize_number + 1) % len(self.exercizes))

    def previous_exercize(self):
        self.set_exercize((self.exercize_number - 1) % len(self.exercizes))

    def random_exercize(self):
        self.set_exercize(random.randint(0, len(self.exercizes) - 1))

    def randomize_exercize(self):
        self.set_exercize(self.exercize_number)

    def run_exercize(self):
        self.result_label.value = "🟡 Exécution en cours"
        # self.result_label.style.background = "orange"
        self.run_button.disabled = True
        try:
            success = self.run_notebook(
                self.notebook,
                answer=[answer_zone.value for answer_zone in self.answer_zone],
                dir=os.path.dirname(self.exercize_name),
            )
            self.result_label.value = (
                "✅ Bonne réponse" if success else "❌ Mauvaise réponse"
            )
            # self.result_label.style.background = "green" if success else "red"
            learning_record = { "student": self.learner,
                               "exercise": self.exercize_name,
                               "success": success,
                               "time": datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')}

        except ExecutionError:
            self.result_label.value = "❌ Erreur à l'exécution"
            # self.result_label.style.background = "red"
            learning_record = { "student": self.learner,
                               "exercise": self.exercize_name,
                               "success": False,
                               "time": datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')}

        finally:
            self.run_button.disabled = False

        with open(self.lrs_url, 'a', encoding="utf-8") as f:
            f.write(str(json.dumps(learning_record)) + "\n")

    def display_exercize(self, notebook):
        with self.exercize_zone:
            self.exercize_zone.clear_output(wait=True)
            i_answer = 0
            for cell in notebook.cells:
                if cell["metadata"].get("nbgrader", {}).get("solution", False):
                    if i_answer > 0:
                        self.answer_zone.append(ipywidgets.Textarea())
                    code = cell["source"]
                    if re.search(answer_regexp, code):
                        self.answer_zone[i_answer].value = ""
                        self.answer_zone[i_answer].rows = 2
                    else:
                        begin = code.split("/// BEGIN SOLUTION")[0]
                        nblines = begin.count('\n')
                        end = code.split("/// END SOLUTION")[-1]
                        nelines = end.count('\n')
                        self.answer_zone[i_answer].value = begin + "\n\n" + end
                        self.answer_zone[i_answer].rows = nblines + 5 + nelines
                    display(self.answer_zone[i_answer])
                    i_answer = i_answer + 1
                elif cell["cell_type"] == "markdown":
                    display(IPython.display.Markdown(cell["source"]))
                else:
                    if "hide-cell" not in cell["metadata"].get("tags", []):
                        display(IPython.display.Code(cell["source"]))

    def randomize_notebook(self, notebook: Notebook) -> Notebook:
        notebook = copy.deepcopy(notebook)
        language = notebook.metadata["kernelspec"]["language"]
        randomizer = Randomizer(language=language)
        for cell in notebook.cells:
            cell["source"] = randomizer.randomize(
                text=cell["source"], is_code=(cell["cell_type"] == "code")
            )
        return notebook

    def run_notebook(self, notebook: Notebook, answer: list[str], dir: str) -> bool:
        notebook = copy.deepcopy(notebook)
        kernel_name = notebook["metadata"]["kernelspec"]["name"]
        i_answer = 0
        for i, cell in enumerate(notebook.cells):
            # If Autograded code cell
            if cell["cell_type"] == "code" and cell["metadata"].get("nbgrader", {}).get(
                "solution", False
            ):
                code = cell["source"]
                if re.search(answer_regexp, code):
                    code = re.sub(answer_regexp, answer[i_answer], code)
                else:
                    code = answer[i_answer]
                notebook.cells[i] = nbformat.v4.new_code_cell(code)
                i_answer = i_answer + 1
        ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name, allow_errors=True)

        owd = os.getcwd()
        try:
            os.chdir(dir)
            result = ep.preprocess(notebook)
        finally:
            os.chdir(owd)

        success = True
        for cell in result[0]["cells"]:
            # If this is a code cell and execution errored
            if cell["cell_type"] == "code" and any(
                output["output_type"] == "error" for output in cell["outputs"]
            ):
                if cell["metadata"].get("nbgrader", {}).get("grade", False):
                    # If Autograded tests cell
                    success = False
                # elif cell["metadata"].get("nbgrader", {}).get("solution", False):
                # TODO: handle autograded answer cell failure
                else:
                    # TODO: handle
                    raise ExecutionError("Execution failed")
        return success
