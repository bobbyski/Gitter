from textual import on, events
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen


class GitMenu(ModalScreen[str]):
    """A modal screen that displays a popup 'Git' menu with remote operations."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def __init__(self, branch: str = ""):
        super().__init__()
        self._branch = branch

    def compose(self) -> ComposeResult:
        on_develop = self._branch == "develop"
        on_feature = self._branch.startswith("feature/") or self._branch.startswith("feat/")
        on_release = self._branch.startswith("release/")

        yield OptionList(
            "Pull",
            "Fetch",
            "Push",
            "---",
            "Commit",
            "---",
            Option("Start Feature", id="start_feature", disabled=not on_develop),
            Option("Finish Feature", id="finish_feature", disabled=not on_feature),
            "---",
            Option("Start Release", id="start_release", disabled=not on_develop),
            Option("Finish Release", id="finish_release", disabled=not on_release),
            id="git_list",
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self, event: events.Click) -> None:
        if event.widget is self:
            self.dismiss(None)
