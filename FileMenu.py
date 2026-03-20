from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen

class FileMenu(ModalScreen):
    """A modal screen that displays a popup 'File' menu."""
    
    DEFAULT_CSS = """
    FileMenu {
        align: left top;
    }
    #menu_list {
        width: 20;
        height: auto;
        margin-top: 1;
        margin-left: 2;
        border: solid white;
        background: $panel;
    }
    """

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
        else:
            # For other options, just close the menu
            self.dismiss()

    def on_click(self) -> None:
        # Close the menu if clicked outside
        self.dismiss()
