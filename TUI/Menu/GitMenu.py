from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen

from TUI.debug.rich_log import GitterLogger


class GitMenu(ModalScreen[str]):
    """A modal screen that displays a popup 'Git' menu with remote operations."""

    def __init__(self, branch: str = ""):
        super().__init__()
        self._branch = branch

    def compose(self) -> ComposeResult:
        on_develop = self._branch == "develop"
        on_feature = self._branch.startswith("feature/") or self._branch.startswith("feat/")

        yield OptionList(
            "Commit",
            "Pull",
            "Fetch",
            "Push",
            "---",
            Option("Start Feature", id="start_feature", disabled=not on_develop),
            Option("Finish Feature", id="finish_feature", disabled=not on_feature),
            id="git_list",
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self) -> None:
        GitterLogger.log("Git menu clicked (GitMenu)")
