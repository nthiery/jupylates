from abc import abstractmethod
import copy, getpass, json, os, random, re
from datetime import datetime
# Why can't this be imported from IPython.display?
#from IPython.core.display_functions import display
from IPython.display import Code, Markdown, display
import ipywidgets  # type: ignore
import io
import nbformat.v4
import jupytext    # type: ignore
from typing import Any, Callable, Dict, Type, Iterator, List, Optional, Union
from nbconvert.preprocessors import ExecutePreprocessor

from code_randomizer import Randomizer


Notebook = Any
Activity = str


class ExecutionError(RuntimeError):
    pass


answer_regexp = re.compile(r"INPUT\(.*\)", re.DOTALL)

format_comment = {
    "C++17": "///",
    "python": "###"
}

lexer = {
    "C++17": "c++",
    "python": "python"
}
begin_end_regexp = re.compile(r"{format_comment} (BEGIN|END) SOLUTION")

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
        None: ''
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
    def __init__(self,
                 activity: Activity,
                 max_score: int = 3,
                 grace_period: int = 2,
                 penalty: int = 1
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
        return self.grade_period + self.max_score // self.penalty

    @property
    def score(self) -> int:
        return self._score

    @property
    def info(self) -> str:
        return f"Score: {self.score}/{self.max_score}; " + \
            f"Tentatives: {self.executions}/{self.max_attempts}"


class LocalLRS(LearningRecordConsumer):
    def __init__(self, file: str, learner: str):
        self.learner = learner
        self.file = file

    def write_event(self, action: str, **args: Any) -> None:
        event = {
            "student": self.learner,
            "action": action,
            **args,
            "time": datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')
        }
        with open(self.file, 'a', encoding="utf-8") as f:
            f.write(str(json.dumps(event)) + "\n")

    def view(self, activity: Activity) -> None:
        self.write_event(action='view',
                         activity=activity)

    def execute(self, activity: Activity, success: bool) -> None:
        self.write_event(action='execute',
                         activity=activity,
                         success=success)

    def replay(self, on: LearningRecordConsumer) -> None:
        """
        Replay all the stored learning records to the consumer
        """
        try:
            with open(self.file, 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    json_record = json.loads(line)
                    if json_record["action"] == "view":
                        on.view(activity=json_record["activity"])
                    if json_record["action"] == "execute":
                        on.execute(activity=json_record["activity"],
                                   success=json_record["success"])
        except FileNotFoundError:
            pass


class ActivitiesStates(LearningRecordConsumer):
    def __init__(self,
                 activities: List[Activity],
                 ActivityStateType: Type
                 ):
        self.activities = activities
        self.states: Dict[Activity, ActivityState] = {
            activity: ActivityStateType(activity)
            for activity in activities
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
            score = score / max_score
            if score <= 0.25:
                color = 'red'
            elif score <= 0.5:
                color = 'orange'
            elif score <= 0.75:
                color = 'yellow'
            else:
                color = 'green'
        else:
            color = 'green'

        badge = anybadge.Badge("score", s, default_color=color)
        with io.open(os.path.join("feedback", "scores.svg"), "w") as fd:
            fd.write(badge.badge_svg_text)


Mode = str  # 'train', 'exam', 'debug'


class Exerciser(ipywidgets.HBox):

    themes: Dict[str, List[str]]
    ActivityStateType: Type[ActivityState]

    def __init__(self,
                 exercises: Union[List[str],
                                  Dict[str, List[str]]],
                 lrs_url: str = '.lrs.json',
                 mode: Mode = 'train'
                 ):
        # learner owner of the session
        learner = os.getenv('JUPYTERHUB_USER')
        if not learner:
            learner = getpass.getuser()
        self.learner: str = learner

        self.start_time = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S%z')

        if isinstance(exercises, list):
            self.themes = {"": exercises}
        else:
            self.themes = exercises

        self.lrs = LocalLRS(file=lrs_url,
                            learner=learner)

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
            options=self.themes.keys(),
            description="Thème")
        if list(self.themes.keys()) == ['']:
            self.theme_chooser.layout.display = 'none'

        # Progress zone
        box_layout = ipywidgets.Layout(border='',
                                       height='',
                                       width='',
                                       flex_flow='column',
                                       display='flex')
        self.progress_zone = ipywidgets.VBox(layout=box_layout)

        # Exercise zone
        border_layout = ipywidgets.Layout(border="solid", padding="1ex")
        self.exercise_zone = ipywidgets.Output(layout=border_layout)
        self.answer_zone = [ipywidgets.Textarea()]

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
        if self.mode != 'debug':
            self.source_link.layout.display = 'none'

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
                    [self.previous_button,
                     self.random_button,
                     self.next_button,
                     self.total_score_view,
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
        self.run_button.on_click(lambda event: self.run_exercise())
        self.theme_chooser.observe(lambda event: self.reset_exercises())

        ######################################################################
        # Initialization
        ######################################################################

        self.reset_exercises()

        super().__init__([
            ipywidgets.VBox(
                [
                    self.theme_chooser,
                    self.progress_zone,
                ]),
            ipywidgets.VBox([
                self.exercise_zone,
                self.controler_zone])])

    def reset_exercises(self) -> None:
        # Model
        self.exercises = sorted(self.themes[self.theme_chooser.value])
        self.exercise_states = ActivitiesStates(
            self.exercises,
            ActivityStateType=self.ActivityStateType
        )
        self.lrs.replay(on=self.exercise_states)

        # View
        item_layout = ipywidgets.Layout(width='auto', height='auto')
        items = [ipywidgets.Button(layout=item_layout,
                                   description=exercise.split("/")[-1])
                 for exercise in self.exercises]
        self.progress_zone.children = items

        # Controller
        def make_button_callback(k: int) -> Callable[[ipywidgets.Button], None]:
            def callback(button: ipywidgets.Button) -> None:
                self.set_exercise(k)
            return callback

        for k in range(len(items)):
            items[k].on_click(make_button_callback(k))

        # Application
        self.set_exercise(0)

    def update_progress_zone(self) -> None:
        buttons = self.progress_zone.children
        for state, button in zip(self.exercise_states,
                                 buttons):
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

    def randomize_exercise(self) -> None:
        self.set_exercise(self.exercise_number)

    def run_exercise(self) -> None:
        self.result_view.value = "🟡 Exécution en cours"
        self.run_button.disabled = True
        try:
            success = self.run_notebook(
                self.notebook,
                answer=[answer_zone.value for answer_zone in self.answer_zone],
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

    def display_exercise(self, notebook: Notebook) -> None:
        language = notebook.metadata["kernelspec"]["language"]
        with self.exercise_zone:
            self.exercise_zone.clear_output(wait=True)
            i_answer = 0
            for cell in notebook.cells:
                if cell["metadata"].get("nbgrader", {}).get("solution", False):
                    if i_answer > 0:
                        self.answer_zone.append(ipywidgets.Textarea())
                    code = cell["source"]
                    if re.search(answer_regexp, code):
                        self.answer_zone[i_answer].value = ""
                        self.answer_zone[i_answer].rows = 2
                        display(self.answer_zone[i_answer])
                    else:
                        for begin in code.split(format_comment[language] + " BEGIN SOLUTION"):
                            end = begin.split(format_comment[language] + " END SOLUTION")
                            if len(end) > 1:
                                self.answer_zone[i_answer].value = (
                                    f"\n{format_comment[language]} COMPLETEZ LA SOLUTION ICI {format_comment[language]}\n"
                                )
                                self.answer_zone[i_answer].rows = 3
                                display(self.answer_zone[i_answer])
                                i_answer = i_answer + 1
                                self.answer_zone.append(ipywidgets.Textarea())
                                display(Code(end[1], language=lexer[language]))
                            else:
                                display(Code(end[0], language=lexer[language]))
                elif cell["cell_type"] == "markdown":
                    display(Markdown(cell["source"]))
                else:
                    if "hide-cell" not in cell["metadata"].get("tags", []):
                        display(Code(cell["source"], language=lexer[language]))

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
        language = notebook.metadata["kernelspec"]["language"]
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
                    solution_code = ""
                    for begin in code.split(format_comment[language] + " BEGIN SOLUTION"):
                        end = begin.split(format_comment[language] + " END SOLUTION")
                        if len(end) > 1:
                            solution_code += answer[i_answer]
                            i_answer = i_answer + 1
                            solution_code += end[1]
                        else:
                            solution_code += end[0]
                    
                    code = solution_code
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
