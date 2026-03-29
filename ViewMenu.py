from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen
from ProjectView import ProjectView
from rich_log import GitterLogger

class ViewMenu(ModalScreen[str]):
    def __init__(self, logs_visible: bool):
        super().__init__()
        self._logs_label = "Hide logs" if logs_visible else "Show logs"

    def compose(self) -> ComposeResult:
        yield OptionList(
            "Refresh",
            "---",
            self._logs_label,
            id="view_list"
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self) -> None:
        GitterLogger.log( "View menu clicked (ViewMenu)" )
