from textual import on, events
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen


class GitMenu(ModalScreen[str]):
    """A modal screen that displays a popup 'Git' menu with remote operations."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def __init__(self, branch: str = "", project_selected: bool = False):
        super().__init__()
        self._branch = branch
        self._project_selected = project_selected

    def compose(self) -> ComposeResult:
        has_project = self._project_selected
        on_develop = self._branch == "develop"
        on_feature = self._branch.startswith("feature/") or self._branch.startswith("feat/")
        on_release = self._branch.startswith("release/")

        yield OptionList(
            Option("Pull",   id="pull",   disabled=not has_project),
            Option("Fetch",  id="fetch",  disabled=not has_project),
            Option("Push",   id="push",   disabled=not has_project),
            Option("Push Master and Develop", id="push_main_develop", disabled=not (has_project and on_develop)),
            "---",
            Option("Commit", id="commit", disabled=not has_project),
            "---",
            Option("Start Feature", id="start_feature", disabled=not (has_project and on_develop)),
            Option("Finish Feature", id="finish_feature", disabled=not (has_project and on_feature)),
            "---",
            Option("Start Release", id="start_release", disabled=not (has_project and on_develop)),
            Option("Finish Release", id="finish_release", disabled=not (has_project and on_release)),
            id="git_list",
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self, event: events.Click) -> None:
        if event.widget is self:
            self.dismiss(None)
