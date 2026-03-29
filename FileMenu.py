from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen

from rich_log import GitterLogger


class FileMenu(ModalScreen):
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
        if str(event.option.prompt) == "Quit":
            self.app.exit()
        # else:
        #     self.dismiss()

    def on_click(self) -> None:
        # Close the menu if clicked outside
        GitterLogger.log( "File menu clicked (FileMenu)" )
