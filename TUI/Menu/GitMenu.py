from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen

from TUI.debug.rich_log import GitterLogger


class GitMenu(ModalScreen[str]):
    """A modal screen that displays a popup 'Git' menu with remote operations."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            "Pull",
            "Fetch",
            "Push",
            id="git_list"
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self) -> None:
        GitterLogger.log("Git menu clicked (GitMenu)")
