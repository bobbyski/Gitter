from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Label
from FileMenu import FileMenu
from MenuBar import MenuBar

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

