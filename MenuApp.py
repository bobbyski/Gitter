from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Static, OptionList, Label
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

class MenuBar(Static):
    """A simple menu bar at the top."""
    
    DEFAULT_CSS = """
    MenuBar {
        dock: top;
        height: 1;
        background: $accent;
        color: $text;
    }
    MenuBar > Horizontal {
        width: 100%;
    }
    MenuBar Label {
        padding: 0 2;
    }
    MenuBar Label:hover {
        background: $accent-darken-2;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("File", id="file_menu_label")
            yield Label("Edit")
            yield Label("View")
            yield Label("Help")

class MenuApp(App):
    """A Textual app with a top menu bar and a 'File' popup menu."""
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "show_file_menu", "File Menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield MenuBar()
        yield Container(Label("Welcome to the Menu App!", id="welcome"), id="main_container")
        yield Footer()

    def action_show_file_menu(self) -> None:
        self.push_screen(FileMenu())

    @on(events.Click, "#file_menu_label")
    def handle_file_click(self) -> None:
        self.push_screen(FileMenu())

if __name__ == "__main__":
    app = MenuApp()
    app.run()

