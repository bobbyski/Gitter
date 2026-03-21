from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Label
from FileMenu import FileMenu
from MenuBar import MenuBar
from ProjectView import ProjectView


class MenuApp(App):
    """A Textual app with a top menu bar and a 'File' popup menu."""
    
    CSS_PATH = ["menu_app.tcss", "project_view.tcss"]

    BINDINGS = [
        ("^q", "quit", "Quit"),
        # ("^f", "show_file_menu", "File Menu"),
    ]

    def compose(self) -> ComposeResult:
        self.project = ProjectView()

        yield Header()
        yield MenuBar()
        # self.mainContainer = Container( Label("Welcome to the Menu App!", id="welcome"), id="main_container")
        self.mainContainer = Container( self.project, classes="main_container", id="main_container")
        yield self.mainContainer
        yield Footer()

    def action_show_file_menu(self) -> None:
        self.push_screen(FileMenu())

    @on(events.Click, "#file_menu_label")
    def handle_file_click(self) -> None:
        self.push_screen(FileMenu())

if __name__ == "__main__":
    app = MenuApp()
    app.run()

