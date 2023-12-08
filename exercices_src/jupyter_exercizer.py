import copy, getpass, json, os, random, re
from datetime import datetime
import IPython  # type: ignore
from IPython.core.display_functions import display  # type: ignore
import ipywidgets  # type: ignore
import nbformat
import jupytext    # type: ignore
from typing import Any, List, Optional
from nbconvert.preprocessors import ExecutePreprocessor  # type: ignore

from code_randomizer import Randomizer


Notebook = Any


class ExecutionError(RuntimeError):
    pass


answer_regexp = re.compile(r"INPUT\(.*\)", re.DOTALL)


class ExercizeState():
    def __init__(self, exercise):
        self.exercize = exercise
        self.viewed = False
        self.executed = False
        self.n_success = 0
        self.n_failure = 0

    def view(self) -> None:
        self.viewed = True

    def execute(self, success: bool) -> None:
        self.executed = True
        if success:
            self.n_success += 1
        else:
            self.n_failure += 1

    def status(self) -> Optional[str]:
        if self.executed:
            if self.n_success > 0:
                return "success"
            else:
                return "failure"
        else:
            if self.viewed:
                return "viewed"
            else:
                return None


state_styles = {
    "viewed": "info",
    "success": "success",
    "failure": "danger",
    None: ''
}


class LocalLRS:
    def __init__(self, file: str, learner: str):
        self.learner = learner
        self.file = file

    def write_event(self, action: str, **args) -> None:
        event = {
            "student": self.learner,
            "action": action,
            **args,
            "time": datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')
        }
        with open(self.file, 'a', encoding="utf-8") as f:
            f.write(str(json.dumps(event)) + "\n")

    def view(self, exercize: str):
        self.write_event(action='view',
                         exercise=exercize)

    def execute(self, exercize: str, success: bool):
        self.write_event(action='execute',
                         exercise=exercize,
                         success=success)


def initialize_exercize_states(exercizes: List[str], lrs_url: str):
    states = {
        exercize: ExercizeState(exercize)
        for exercize in exercizes
    }
    try:
        with open(lrs_url, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                json_record = json.loads(line)
                state = states.get(json_record["exercise"], None)
                if state is None:
                    continue

                if json_record["action"] == "view":
                    state.view()
                if json_record["action"] == "execute":
                    state.execute(success=json_record["success"])
    except FileNotFoundError:
        pass

    return [states[exercize]
            for exercize in exercizes]


class Exercizer(ipywidgets.HBox):
    def __init__(self,
                 exercizes: List[str],
                 lrs_url: str = ".learning_record.json"):
        # learner owner of the session
        learner = os.getenv('JUPYTERHUB_USER')
        if not learner:
            learner = getpass.getuser()
        self.learner: str = learner

        self.start_time = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')

        self.exercizes = sorted(exercizes)

        self.exercize_states = initialize_exercize_states(self.exercizes, lrs_url)

        self.lrs = LocalLRS(file=lrs_url,
                            learner=learner)

        item_layout = ipywidgets.Layout(width='auto', height='auto')
        items = [ipywidgets.Button(layout=item_layout,
                                   description=self.exercizes[i].split("/")[-1])
                 for i in range(len(self.exercizes))]

        box_layout = ipywidgets.Layout(border='',
                            height='',
                            width='',
                            flex_flow='column',
                            display='flex')
        carousel = ipywidgets.VBox(children=items, layout=box_layout)
        self.progress_zone = carousel

        # View
        border_layout = ipywidgets.Layout(border="solid", padding="1ex")
        self.exercize_zone = ipywidgets.Output(layout=border_layout)
        self.answer_zone = [ipywidgets.Textarea()]
        self.run_button = ipywidgets.Button(
            description="Valider", button_style="primary", icon="check"
        )
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

        def make_button_callback(k):
            def callback(button):
                self.set_exercize(k)
            return callback

        for k in range(len(items)):
            items[k].on_click(make_button_callback(k))

        # Initialize
        self.set_exercize(0)
        self.update_progress_zone()

        super().__init__([
            self.progress_zone,
            ipywidgets.VBox([
                self.exercize_zone,
                self.controler_zone])])

    def update_progress_zone(self):
        buttons = self.progress_zone.children
        for state, button in zip(self.exercize_states,
                                 buttons):
            button.button_style = state_styles[state.status()]
            button.icon = "play" if state.exercize == self.exercize_name else ""

    def set_exercize(self, i: int):
        self.exercize_number = i
        self.exercize_name = self.exercizes[self.exercize_number]
        self.notebook = self.randomize_notebook(jupytext.read(self.exercize_name))
        self.display_exercize(self.notebook)
        self.result_label.value = ""

        self.exercize_states[self.exercize_number].view()
        self.update_progress_zone()
        self.lrs.view(self.exercize_name)

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
        except ExecutionError:
            self.result_label.value = "❌ Erreur à l'exécution"
        finally:
            self.run_button.disabled = False

        state = self.exercize_states[self.exercize_number]
        state.execute(success=success)
        self.update_progress_zone()
        self.lrs.execute(exercize=self.exercize_name,success=success)

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

    def run_notebook(self, notebook: Notebook, answer: List[str], dir: str) -> bool:
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
