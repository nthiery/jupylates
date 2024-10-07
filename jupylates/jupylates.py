from abc import abstractmethod
import copy, getpass, json, os, random, re
from datetime import datetime, date

# Why can't this be imported from IPython.display?
# from IPython.core.display_functions import display
from IPython.display import Code, Markdown, HTML, display
import ipywidgets  # type: ignore
import io
import nbformat.v4
import jupytext  # type: ignore
from typing import Any, Callable, Dict, Type, Iterator, List, Optional, Union
from nbconvert.preprocessors import ExecutePreprocessor
from jupyter_client import KernelClient, KernelManager  # type: ignore

from .code_randomizer import Randomizer

# recommender fsrs / SM2 and 2 Machine learning
from .recommender.sm2 import rec_SM2
from .recommender.machine.ml_maison import maison
from .recommender.machine.ml_maison_time import maison_time
from .recommender.fsrs.fsrs import rec_fsrs

Notebook = Any
Activity = str


class ExecutionError(RuntimeError):
    pass


answer_regexp = re.compile(r"INPUT\(.*\)", re.DOTALL)
answer_solution_regexp = re.compile(r"INPUT_(?P<type>\w+)\(\"(?P<description>.*?)\",\s+(?P<args>(\w+,\s+)*)(?P<solution>[^,$]*)\)", re.DOTALL)
eval_regexp = re.compile("{eval}`(.*?)`")


def test_answer_solution_regexp() -> None:
    from jupylates.jupylates import answer_solution_regexp
    match = re.search(answer_solution_regexp, 'answer, solution = INPUT_TEXT("x", foo()) lorem ipsum')
    assert match is not None
    assert match.group('type') == "TEXT"
    assert match.group('description') == "x"
    assert match.group('args') == ""
    assert match.group('solution') == "foo()"

    match = re.search(answer_solution_regexp, 'lorem INPUT_EXPR("xxx", answer, solution, foo()) ipsum')
    assert match is not None
    assert match.group('type') == "EXPR"
    assert match.group('description') == "xxx"
    assert match.group('args') == "answer, solution, "
    assert match.group('solution') == "foo()"

def write_literal_python(literal: Any):
    if isinstance(literal, bool):
        return str(literal)
    else:
        return json.dumps(literal)

write_literal = {"C++17": json.dumps, "python": write_literal_python}
format_comment = {"C++17": "///", "python": "###"}

lexer = {"C++17": "c++", "python": "python"}
begin_end_regexp = re.compile(r"{format_comment} (BEGIN|END) SOLUTION")

# TODO: find a better place for this
# Ref: https://stackoverflow.com/questions/75114841/debugger-warning-from-ipython-frozen-modules

os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"


def execute_code(
    kernel_client: KernelClient, code: str
) -> List[Dict[str, Dict[str, str]]]:
    # print(f"executing {cell['source']}")
    kernel_client.execute(code=code)
    outputs = []
    while True:
        msg = kernel_client.get_iopub_msg()
        # print(msg)
        if msg["msg_type"] == "status":
            execution_state = msg["content"]["execution_state"]
            if execution_state in {"starting", "busy"}:
                continue
            elif execution_state == "idle":
                break
            else:
                assert False
        if msg["msg_type"] == "execute_input":
            continue
        if msg["msg_type"] in ["execute_result", "error"]:
            content = copy.copy(msg["content"])
            content["output_type"] = msg["msg_type"]
            outputs.append(content)
    return outputs


def display_outputs(outputs: List[dict]) -> None:
    for output in outputs:
        if output["output_type"] == "error":
            display(output["ename"])
        elif "text/html" in output["data"]:
            display(HTML(output["data"]["text/plain"]))
        elif "text/plain" in output["data"]:
            print(output["data"]["text/plain"])
        else:
            display(output)


def execute_code_and_return_single_output(
    kernel_client: KernelClient, code: str
) -> str:
    """
    Execute the code in the kernel and return its output

    There should be a single output, which is returned as an html string.
    """
    outputs = execute_code(kernel_client, code)
    assert len(outputs) == 1
    (output,) = outputs
    if "text/html" in output["data"]:
        return output["data"]["text/html"]
    if "text/plain" in output["data"]:
        s = output["data"]["text/plain"]
        if False and "\n" in s:  # minimal multiline support
            s = f"```\n{s}\n```"
        return s
    assert False, f"Unsupported data types {output['data'].keys()}"


def substitute(source: str, substitutions: Dict[str, str]) -> str:
    """
    Subtitute `substitutions` in the `source`

    For each pair (key, value) in the substitution dictionary, replace
    all occurences of the key appearing as a full word in the source
    by the corresponding value.
    """
    if not substitutions:
        return source
    pattern = re.compile(r"\b(" + "|".join(substitutions.keys()) + r")\b")
    return pattern.sub(lambda i: substitutions[i.group()], source)


class ActivityLearningRecordConsumer:
    """
    A consumer of events on an activity
    """

    @abstractmethod
    def view(self) -> None:
        """
        The activity has been viewed by the learner
        """

    @abstractmethod
    def execute(self, success: bool) -> None:
        """
        The activity has been executed by the learner

        Parameters
        ----------
        success: bool
            Whether the activity was executed successfully
        """


class LearningRecordConsumer:
    """
    A consumer of events on a collection of activities
    """

    @abstractmethod
    def view(self, activity: Activity) -> None:
        """
        The given activity has been viewed by the learner
        """

    @abstractmethod
    def execute(self, activity: Activity, success: bool) -> None:
        """
        The given activity has been executed by the learner
        """


class ActivityState(ActivityLearningRecordConsumer):
    """
    A consumer that defines the state of an activity from the stream
    of events that was received
    """

    activity: Activity

    def __init__(self, activity: Activity):
        self.activity = activity

    @property
    @abstractmethod
    def status(self) -> Optional[str]:
        """
        The current status of the activity
        """
        return None

    @property
    @abstractmethod
    def score(self) -> int:
        """
        The current score for the activity
        """

    """
    The maximum score for the activity
    """
    max_score: int

    styles = {
        "viewed": "info",
        "success": "success",
        "failure": "warning",
        "game over: success": "success",
        "game over: failure": "danger",
        None: "",
    }

    @property
    def style(self) -> Optional[str]:
        return self.styles[self.status]

    @property
    def disabled(self) -> bool:
        return self.status is not None and self.status.startswith("game over")

    @property
    def info(self) -> str:
        """
        A human readable summary of the current state
        """
        return f"Score: {self.score}"


class ActivityStateCounter(ActivityState):
    """
    This activity state counts views, executions, successes and failures.

    With the default implementation of `status` and `score`, the
    status of the activity is a success and the score is 1 as soon as
    the execution was successful at least once.

    Examples
    --------

        >>> state = ActivityStateCounter("my activity")
        >>> state.views
        0
        >>> state.executions
        0
        >>> state.successes
        0
        >>> state.failures
        0
        >>> state.status
        >>> state.score
        0

        >>> state.view()
        >>> state.status
        'viewed'

        >>> state.views
        1
        >>> state.failures
        0
        >>> state.successes
        0

        >>> state.execute(success=False)
        >>> state.execute(success=False)
        >>> state.status
        'failure'
        >>> state.score
        0

        >>> state.execute(success=True)
        >>> state.status
        'success'
        >>> state.execute(success=False)
        >>> state.status
        'success'
        >>> state.score
        1

        >>> state.views
        1
        >>> state.executions
        4
        >>> state.failures
        3
        >>> state.successes
        1

    The default implementation
    """

    def __init__(self, activity: Activity):
        super().__init__(activity)
        self.views = 0
        self.executions = 0
        self.successes = 0
        self.failures = 0

    def view(self) -> None:
        self.views += 1

    def execute(self, success: bool) -> None:
        self.executions += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1

    @property
    def status(self) -> Optional[str]:
        if self.successes:
            return "success"
        elif self.failures:
            return "failure"
        elif self.views:
            return "viewed"
        else:
            return None

    @property
    def score(self) -> int:
        return 1 if self.successes else 0

    max_score: int = 1


class ActivityStateInitialFailurePenalty(ActivityStateCounter):
    """
    This activity state defines the score according to the number of
    failures before the first success.

    Initially, the score is zero. The max score is granted if the
    learner succeeds within `grace_period` attempts. A penalty of
    `penalty` is removed for every additional failure, and the status
    set to "failure". If the learner succeeds before the accumulated
    penalties exeed the maximal score, then the score is set
    accordingly, and the status is "success". Otherwise, the status is
    "done".

    Examples
    --------

        >>> state = ActivityStateInitialFailurePenalty("my activity", max_score=7)
        >>> state.score
        0
        >>> state.status
        >>> state.view()
        >>> state.status
        'viewed'
        >>> state.execute(success=True)
        >>> state.score
        7
        >>> state.status
        'success'

        >>> state = ActivityStateInitialFailurePenalty("my activity", max_score=7)
        >>> state.execute(success=False)
        >>> state.score
        0
        >>> state.status
        'failure'
        >>> state.execute(success=True)
        >>> state.score
        7
        >>> state.status
        'success'

        >>> state = ActivityStateInitialFailurePenalty("my activity", max_score=3, penalty=2)
        >>> state.execute(success=False)
        >>> state.execute(success=False)
        >>> state.execute(success=True)
        >>> state.score
        1
        >>> state.status
        'success'

        >>> state = ActivityStateInitialFailurePenalty("my activity", max_score=2, penalty=2)
        >>> state.execute(success=False)
        >>> state.execute(success=False)
        >>> state.execute(success=False)
        >>> state.score
        0
        >>> state.status
        'done'
        >>> state.execute(success=True)
        >>> state.score
        0
        >>> state.status
        'done'
    """

    def __init__(
        self,
        activity: Activity,
        max_score: int = 3,
        grace_period: int = 2,
        penalty: int = 1,
    ):
        super().__init__(activity)
        self.max_score = max_score
        self.potential_score = max_score
        self.grade_period = grace_period
        self.penalty = penalty
        # Note: in this class, one would want to implement `score` by
        # an attribute; however apparently one can't override a
        # property with an attribute; so we use a private attribute.
        self._score: int = 0
        self.views: int = 0
        self.executions: int = 0

    def view(self) -> None:
        self.views += 1

    def execute(self, success: bool) -> None:
        self.executions += 1
        if success:
            if self.score == 0 and self.potential_score > 0:
                self._score = self.potential_score
        else:
            if self.executions >= self.grade_period:
                self.potential_score -= self.penalty

    @property
    def status(self) -> Optional[str]:
        if self.score:
            return "game over: success"
        elif self.potential_score <= 0:
            return "game over: failure"
        elif self.executions:
            return "failure"
        elif self.views:
            return "viewed"
        else:
            return None

    @property
    def max_attempts(self) -> int:
        return self.grade_period + (self.max_score - 1) // self.penalty

    @property
    def score(self) -> int:
        return self._score

    @property
    def info(self) -> str:
        return (
            f"Score: {self.score}/{self.max_score}; "
            + f"Tentatives: {self.executions}/{self.max_attempts}"
        )


class LocalLRS(LearningRecordConsumer):
    def __init__(self, file: str, learner: str):
        self.learner = learner
        self.file = file

    def write_event(self, action: str, **args: Any) -> None:
        event = {
            "student": self.learner,
            "action": action,
            **args,
            "time": datetime.utcnow().strftime("%Y-%m-%d-%H%M%S%z"),
        }
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(str(json.dumps(event)) + "\n")

    def view(self, activity: Activity) -> None:
        self.write_event(action="view", activity=activity)

    def execute(self, activity: Activity, success: bool) -> None:
        self.write_event(action="execute", activity=activity, success=success)

    def replay(self, on: LearningRecordConsumer) -> None:
        """
        Replay all the stored learning records to the consumer
        """
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    json_record = json.loads(line)
                    if json_record["action"] == "view":
                        on.view(activity=json_record["activity"])
                    if json_record["action"] == "execute":
                        on.execute(
                            activity=json_record["activity"],
                            success=json_record["success"],
                        )
        except FileNotFoundError:
            pass


class ActivitiesStates(LearningRecordConsumer):
    def __init__(self, activities: List[Activity], ActivityStateType: Type):
        self.activities = activities
        self.states: Dict[Activity, ActivityState] = {
            activity: ActivityStateType(activity) for activity in activities
        }

    # TODO: rethink the container API; currently this is similar
    # but not equivalent as the dict API.
    def __iter__(self) -> Iterator[ActivityState]:
        for activity in self.activities:
            yield self.states[activity]

    def __getitem__(self, activity: Activity) -> ActivityState:
        return self.states[activity]

    def view(self, activity: Activity) -> None:
        if activity in self.states:
            self.states[activity].view()

    def execute(self, activity: Activity, success: bool) -> None:
        if activity in self.states:
            self.states[activity].execute(success=success)

    @property
    def score(self) -> int:
        return sum(state.score for state in self.states.values())

    @property
    def max_score(self) -> int:
        return sum(state.max_score for state in self.states.values())

    @property
    def info(self) -> str:
        return f"Total score: {self.score} / {self.max_score}"

    def export_score(self, assignment_name: str, student: str) -> None:
        score = self.score
        max_score = self.max_score
        os.makedirs("feedback", exist_ok=True)
        with io.open(os.path.join("feedback", "scores.csv"), "w") as fd:
            fd.write("student, assignment, notebook, total_score, max_total_score\n")
            fd.write(f"{student}, {assignment_name}, index, {score}, {max_score}\n")

        import anybadge  # type: ignore

        s = f"total: {score:g}/{max_score:g}"

        if max_score > 0:
            normalized_score = score / max_score
            if normalized_score <= 0.25:
                color = "red"
            elif normalized_score <= 0.5:
                color = "orange"
            elif normalized_score <= 0.75:
                color = "yellow"
            else:
                color = "green"
        else:
            color = "green"

        badge = anybadge.Badge("score", s, default_color=color)
        with io.open(os.path.join("feedback", "scores.svg"), "w") as fd:
            fd.write(badge.badge_svg_text)


Mode = str  # 'train', 'exam', 'debug'


class Exerciser(ipywidgets.HBox):

    themes: Dict[str, List[str]]
    ActivityStateType: Type[ActivityState]

    kernel_manager: Optional[KernelManager] = None

    def __init__(
        self,
        exercises: Union[List[str], Dict[str, List[str]]],
        lrs_url: str = ".lrs.json",
        mode: Mode = "train",
    ):
        # learner owner of the session
        learner = os.getenv("JUPYTERHUB_USER")
        if not learner:
            learner = getpass.getuser()
        self.learner: str = learner

        self.start_time = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S%z")

        if isinstance(exercises, list):
            self.themes = {"": exercises}
        else:
            self.themes = exercises

        self.lrs = LocalLRS(file=lrs_url, learner=learner)

        self.mode = mode
        if mode == "exam":
            self.ActivityStateType = ActivityStateInitialFailurePenalty
        else:
            self.ActivityStateType = ActivityStateCounter

        ######################################################################
        # View
        ######################################################################

        # Theme chooser
        self.theme_chooser = ipywidgets.Dropdown(
            options=self.themes.keys(), description="Thème"
        )
        if list(self.themes.keys()) == [""]:
            self.theme_chooser.layout.display = "none"

        # Recommender chooser
        options_rec = ["FSRS", "SM2", "Maison", "Maison-time"]
        for exercice in list(self.themes.values())[0]:
            if not os.path.exists(os.getcwd() + "/models/" + exercice[:-2] + "pkl"):
                # print(f"{exercice[:-2]+'pkl'} model not found")  #DEBUG
                options_rec = ["FSRS", "SM2"]
        actual_theme = exercice.split("/")[0]
        # print(actual_theme) # DEBUG

        self.rec_chooser = ipywidgets.Dropdown(
            options=options_rec,
            description="Recommendeurs :",
            style={"description_width": "initial"},
            layout={"width": "max-content"},
        )

        # Progress zone
        box_layout = ipywidgets.Layout(
            border="", height="", width="", flex_flow="column", display="flex"
        )
        self.progress_zone = ipywidgets.VBox(layout=box_layout)

        # Exercise zone
        border_layout = ipywidgets.Layout(border="solid", padding="1ex")
        self.exercise_zone = ipywidgets.Output()
        self.exercise_zone_final_output = ipywidgets.Output()

        # Controler zone
        self.run_button = ipywidgets.Button(
            description="Valider", button_style="primary", icon="check"
        )
        self.result_view = ipywidgets.Label()
        self.score_view = ipywidgets.Label()
        self.total_score_view = ipywidgets.Label()
        self.randomize_button = ipywidgets.Button(
            icon="dice",
            description="Variante",
            tooltip="Tire aléatoirement une autre variante du même exercice",
            button_style="primary",
            layout={"width": "fit-content"},
        )
        self.recommendeur_button = ipywidgets.Button(
            icon="fa-thumbs-o-up",
            description="Recommender",
            tooltip="Sort un exercice recommandé pour vous",
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

        self.source_link = ipywidgets.Output()
        if self.mode != "debug":
            self.source_link.layout.display = "none"

        self.controler_zone = ipywidgets.VBox(
            [
                ipywidgets.HBox(
                    [
                        self.randomize_button,
                        self.run_button,
                        self.score_view,
                        self.result_view,
                    ]
                ),
                ipywidgets.HBox(
                    [
                        self.previous_button,
                        self.random_button,
                        self.next_button,
                        self.total_score_view,
                    ]
                ),
                ipywidgets.HBox(
                    [
                        self.rec_chooser,
                        self.recommendeur_button,
                    ]
                ),
                self.source_link,
            ]
        )

        ######################################################################
        # Controller
        ######################################################################

        self.next_button.on_click(lambda event: self.next_exercise())
        self.previous_button.on_click(lambda event: self.previous_exercise())
        self.random_button.on_click(lambda event: self.random_exercise())
        self.randomize_button.on_click(lambda event: self.randomize_exercise())
        self.recommendeur_button.on_click(
            lambda event: self.recommendeur_exercise(actual_theme)
        )
        self.run_button.on_click(lambda event: self.run_exercise())
        self.theme_chooser.observe(lambda event: self.reset_exercises(), names="value")

        ######################################################################
        # Initialization
        ######################################################################

        self.reset_exercises()

        super().__init__(
            [
                ipywidgets.VBox(
                    [
                        self.theme_chooser,
                        self.progress_zone,
                    ]
                ),
                ipywidgets.VBox(
                    [
                        ipywidgets.VBox(
                            [
                                self.exercise_zone,
                                self.exercise_zone_final_output,
                            ],
                            layout=border_layout,
                        ),
                        self.controler_zone,
                    ]
                ),
            ]
        )

    def reset_exercises(self) -> None:
        # Model
        self.exercises = sorted(self.themes[self.theme_chooser.value])
        self.exercise_states = ActivitiesStates(
            self.exercises, ActivityStateType=self.ActivityStateType
        )
        self.lrs.replay(on=self.exercise_states)

        # View
        item_layout = ipywidgets.Layout(width="auto", height="auto")
        items = [
            ipywidgets.Button(layout=item_layout, description=exercise.split("/")[-1])
            for exercise in self.exercises
        ]
        self.progress_zone.children = items

        # Controller
        def make_button_callback(k: int) -> Callable[[ipywidgets.Button], None]:
            def callback(button: ipywidgets.Button) -> None:
                self.set_exercise(k)

            return callback

        for k in range(len(items)):
            items[k].on_click(make_button_callback(k))

        # Application
        if self.exercises:
            self.set_exercise(0)

    def update_progress_zone(self) -> None:
        buttons = self.progress_zone.children
        for state, button in zip(self.exercise_states, buttons):
            button.button_style = state.style
            button.disabled = state.disabled
            button.icon = "play" if state.activity == self.exercise_name else ""

    def update_score(self) -> None:
        states = self.exercise_states
        self.total_score_view.value = states.info
        state = self.exercise_states[self.exercise_name]
        self.score_view.value = state.info

    def update_exercize_link(self) -> None:
        file = self.exercise_name
        self.source_link.clear_output(wait=True)
        with self.source_link:
            display(Markdown(f"Source: [{file}]({file})"))

    def set_exercise(self, i: int) -> None:
        self.exercise_number = i
        self.exercise_name = self.exercises[self.exercise_number]
        self.notebook = self.randomize_notebook(jupytext.read(self.exercise_name))
        self.display_exercise(self.notebook)
        self.result_view.value = ""

        self.exercise_states[self.exercise_name].view()
        self.update_progress_zone()
        self.update_score()
        self.update_exercize_link()
        self.lrs.view(self.exercise_name)

    def next_exercise(self) -> None:
        self.set_exercise((self.exercise_number + 1) % len(self.exercises))

    def previous_exercise(self) -> None:
        self.set_exercise((self.exercise_number - 1) % len(self.exercises))

    def random_exercise(self) -> None:
        self.set_exercise(random.randint(0, len(self.exercises) - 1))

    def recommendeur_exercise(self, actual_theme) -> None:
        if self.rec_chooser.value == "SM2":
            self.set_exercise(list(self.exercises).index(rec_SM2(list(self.exercises))))
        if self.rec_chooser.value == "FSRS":
            self.set_exercise(
                list(self.exercises).index(rec_fsrs(list(self.exercises)))
            )
        if self.rec_chooser.value == "Maison":
            self.set_exercise(
                list(self.exercises).index(maison(list(self.exercises), actual_theme))
            )
        if self.rec_chooser.value == "Maison-time":
            self.set_exercise(
                list(self.exercises).index(
                    maison_time(list(self.exercises), actual_theme)
                )
            )

    def randomize_exercise(self) -> None:
        self.set_exercise(self.exercise_number)

    def run_exercise(self) -> None:
        self.result_view.value = "🟡 Exécution en cours"
        self.run_button.disabled = True
        try:
            success = self.run_notebook(
                self.notebook,
                answers=[answer_zone.value for answer_zone in self.answer_zone],
                dir=os.path.dirname(self.exercise_name),
            )
        except ExecutionError:
            success = False
            self.result_view.value = "❌ Erreur à l'exécution"
        else:
            self.result_view.value = (
                "✅ Bonne réponse" if success else "❌ Mauvaise réponse"
            )
        finally:
            self.run_button.disabled = False

        state = self.exercise_states[self.exercise_name]
        state.execute(success=success)
        self.update_progress_zone()
        self.update_score()
        self.lrs.execute(activity=self.exercise_name, success=success)

    preheated_kernel_manager_pool: Dict[str, KernelManager] = {}

    def reset_kernel_client(self, kernel_name: str) -> None:
        """
        (Re)set the kernel client in self.kernel_client
        """

        def preheated_kernel_manager(kernel_name: str) -> KernelManager:
            km = KernelManager(kernel_name=kernel_name)
            km.start_kernel()
            return km

        # Stop preview kernel client if alive
        if self.kernel_manager is not None and self.kernel_manager.is_alive():
            self.kernel_manager.shutdown_kernel()

        # Use a preheated kernel manager if available or create one
        if kernel_name in self.preheated_kernel_manager_pool:
            self.kernel_manager = self.preheated_kernel_manager_pool[kernel_name]
        else:
            self.kernel_manager = preheated_kernel_manager(kernel_name)

        # Preheat a kernel manager for next time
        self.preheated_kernel_manager_pool[kernel_name] = preheated_kernel_manager(
            kernel_name
        )

        self.kernel_client = self.kernel_manager.client()

    def display_exercise(self, notebook: Notebook) -> None:
        kernel_name = notebook.metadata["kernelspec"]["name"]
        self.reset_kernel_client(kernel_name)

        language = notebook.metadata["kernelspec"]["language"]
        self.answer_zone: List[ipywidgets.Textarea] = []
        self.substitutions: Dict[str, str] = {}
        with self.exercise_zone:
            self.exercise_zone.clear_output(wait=True)
            self.exercise_zone_final_output.clear_output()
            self.first_answer_cell: Optional[int] = None
            for i_cell, cell in enumerate(notebook.cells):
                cell_tags = cell["metadata"].get("tags", [])

                source = substitute(cell["source"], self.substitutions)

                if "solution" in cell_tags and self.mode == "debug": # != "exam":
                    # TODO: handle INPUT_XXX
                    # Display solution cell
                    assert cell["cell_type"] == "code"
                    display(
                        Markdown(
                            f""":::{{admonition}} Solution
:class: dropdown
```{lexer[language]}
{source}
```
"""
                        )
                    )

                if "answer" in cell_tags:
                    # Handle answer cell
                    assert cell["cell_type"] == "code"
                    if self.first_answer_cell is None:
                        self.first_answer_cell = i_cell
                    code = source
                    if answer_regexp.search(code):
                        textarea = ipywidgets.Textarea()
                        textarea.rows = 2
                        display(textarea)
                        self.answer_zone.append(textarea)
                    elif answer_solution_regexp.search(code):
                        for match in answer_solution_regexp.finditer(code):
                            type = match.group('type')
                            description = match.group('description')
                            if type in ["TEXT", "EXPR"]:
                                inputarea = ipywidgets.Text(description=description)
                            elif type == "INT":
                                inputarea = ipywidgets.IntText(description=description)
                            elif type == "FLOAT":
                                inputarea = ipywidgets.FloatText(description=description)
                            elif type == "BOOL":
                                inputarea = ipywidgets.RadioButtons(options=[("Vrai", True), ("Faux", False)])
                            else:
                                raise ValueError(f"Unknown function INPUT_{type}")
                            display(inputarea)
                            self.answer_zone.append(inputarea)
                    else:
                        zones = code.split(format_comment[language] + " BEGIN SOLUTION")
                        if len(zones) <= 1:
                            textarea = ipywidgets.Textarea()
                            textarea.rows = len(code.splitlines()) + 1
                            display(textarea)
                            self.answer_zone.append(textarea)
                        else:
                            display(Code(zones[0], language=lexer[language]))
                        for zone in zones[1:]:
                            end = zone.split(format_comment[language] + " END SOLUTION")
                            assert len(end) == 2
                            textarea = ipywidgets.Textarea()
                            # textarea.value = f"\n{format_comment[language]} COMPLETEZ LA SOLUTION ICI {format_comment[language]}\n"
                            textarea.rows = len(end[0].splitlines()) + 1
                            self.answer_zone.append(textarea)
                            display(textarea)
                            display(Code(end[1], language=lexer[language]))
                if (
                    cell["cell_type"] == "markdown"
                    and "hide-cell" not in cell_tags
                    and (self.mode == "debug" or "learning objectives" not in cell_tags)
                ):
                    # Display markdown cell

                    def eval(match: re.Match[str]) -> str:
                        code = match[1]
                        return execute_code_and_return_single_output(
                            self.kernel_client, code
                        )

                    source = re.sub(eval_regexp, eval, source)
                    display(Markdown(source))

                if cell["cell_type"] == "code" and "answer" not in cell_tags:
                    # Handle code cell
                    if self.first_answer_cell is None:
                        outputs = execute_code(self.kernel_client, source)
                    else:
                        outputs = []
                    if "substitutions" in cell_tags:
                        assert len(outputs) == 1
                        output = outputs[0]["data"]["text/plain"]
                        self.substitutions.update(json.loads(output[1:-1]))
                        outputs = []
                    if "hide-cell" not in cell_tags and "hide-input" not in cell_tags:
                        display(Code(source, language=lexer[language]))
                    if "hide-cell" not in cell_tags and "hide-output" not in cell_tags:
                        display_outputs(outputs)

    def randomize_notebook(self, notebook: Notebook) -> Notebook:
        """
        Prepare the notebook

        - Randomization
        - Convert nbgrader metadata to tags
        """
        notebook = copy.deepcopy(notebook)
        language = notebook.metadata["kernelspec"]["language"]
        randomizer = Randomizer(language=language)
        for cell in notebook.cells:
            cell["source"] = randomizer.randomize(
                text=cell["source"], is_code=(cell["cell_type"] == "code")
            )
            cell_tags = cell["metadata"].get("tags", [])
            # Compatibility with nbgrader
            if cell["cell_type"] == "code":
                if cell["metadata"].get("nbgrader", {}).get("solution", False):
                    cell_tags.extend(["answer", "solution"])
                elif cell["metadata"].get("nbgrader", {}).get("grade", False):
                    cell_tags.append("test")

            # Sanity checks
            # Should raise proper errors
            #assert not ("test" in cell_tags and "answer" in cell_tags)
            assert not ("hide-cell" in cell_tags and "answer" in cell_tags)

            if cell_tags:
                cell["metadata"]["tags"] = cell_tags

        # temporary backward compatibility
        all_tags = {
            tag for cell in notebook.cells for tag in cell["metadata"].get("tags", [])
        }
        if "answer" not in all_tags:
            assert "solution" in all_tags
            for cell in notebook.cells:
                if "solution" in cell["metadata"].get("tags", []):
                    cell["metadata"]["tags"].append("answer")

        return notebook

    def run_notebook(self, notebook: Notebook, answers: List[str], dir: str) -> bool:
        notebook = copy.deepcopy(notebook)
        language = notebook.metadata["kernelspec"]["language"]

        get_next_answer = answers.__iter__().__next__

        success = True
        # Currentl limitation: the output of the first answer cell and
        # subsequent cells are currently all put together in the same
        # output widget after the exercize zone, instead of appearing
        # each just after the cell that produced it. So only notebooks
        # without visible cells after the first answer cell are
        # properly supported.
        self.exercise_zone_final_output.clear_output()
        assert self.first_answer_cell is not None
        for i in range(self.first_answer_cell, len(notebook.cells)):
            cell = notebook.cells[i]
            cell_tags = cell["metadata"].get("tags", [])
            cell["source"] = substitute(cell["source"], self.substitutions)

            # Prepare answer cells
            if cell["cell_type"] == "code" and "answer" in cell_tags:
                code = cell["source"]
                if re.search(answer_regexp, code):
                    code = re.sub(answer_regexp, get_next_answer(), code)
                elif re.search(answer_solution_regexp, code):
                    def replacement(match: re.Match[str]) -> str:
                        type = match.group('type')
                        description = match.group('description')
                        args = match.group('args')
                        solution = match.group('solution')
                        answer = get_next_answer()
                        if type != "EXPR":
                            answer = write_literal[language](answer)
                        return f'INPUT_{type}("{description}", {args}{answer}, {solution})'

                    code = re.sub(answer_solution_regexp, replacement, code)
                else:
                    zones = code.split(format_comment[language] + " BEGIN SOLUTION")
                    if len(zones) <= 1:
                        code = get_next_answer()
                    else:
                        code = zones[0]
                        for zone in zones[1:]:
                            end = zone.split(format_comment[language] + " END SOLUTION")
                            assert len(end) == 2
                            code += get_next_answer()
                            code += end[1]

                print(code)
                cell["source"] = code

            # Handle code cells
            if cell["cell_type"] == "code":
                outputs = execute_code(self.kernel_client, cell["source"])
                if "hide-cell" not in cell_tags and "hide-output" not in cell_tags:
                    with self.exercise_zone_final_output:
                        display_outputs(outputs)

                # If execution errored
                if any(output["output_type"] == "error" for output in outputs):
                    if "test" in cell_tags:
                        # If Autograded tests cell
                        success = False
                    else:
                        # TODO: handle failures in other cell types
                        raise ExecutionError("Execution failed")

        return success
