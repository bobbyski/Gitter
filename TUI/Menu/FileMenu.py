from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen

from TUI.debug.rich_log import GitterLogger


class FileMenu(ModalScreen[str]):
    """A modal screen that displays a popup 'File' menu."""

    def compose(self) -> ComposeResult:
        yield OptionList(
            "New",
            "Open",
            "Save",
            "---",
            "Quit",
            id="menu_list"
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        option = str(event.option.prompt)
        if option == "Quit":
            self.app.exit()
        else:
            self.dismiss(option)

    def on_click(self) -> None:
        # Close the menu if clicked outside
        GitterLogger.log( "File menu clicked (FileMenu)" )
