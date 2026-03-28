from pathlib import Path

from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Label

from BusinessLogic.GitManager import GitManager
from FileMenu import FileMenu
from MenuBar import MenuBar
from ProjectView import ProjectView
from ViewMenu import ViewMenu
from model.MainFile import MainFile
from model.MainFileManager import MainFileManager
from rich_log import RichLogWindow


class MenuApp(App):
    """A Textual app with a top menu bar and a 'File' popup menu."""
    
    CSS_PATH = ["menu_app.tcss", "project_view.tcss"]

    BINDINGS = [
        ("^q", "quit", "Quit"),
        # ("^f", "show_file_menu", "File Menu"),
    ]

    def compose(self) -> ComposeResult:
        self.project = ProjectView()
        self.logWindow = RichLogWindow()

        yield Header()
        yield MenuBar()
        self.mainContainer = Container( self.project, self.logWindow, classes="main_container", id="main_container")
        # self.mainContainer = Container( self.logWindow, self.project, classes="main_container", id="main_container")
        # self.mainContainer = Container( self.logWindow, classes="main_container", id="main_container")
        yield self.mainContainer
        yield Footer()

    def action_show_file_menu(self) -> None:
        self.push_screen(FileMenu())

    @on(events.Click, "#file_menu_label")
    def handle_file_click(self) -> None:
        self.push_screen(FileMenu())

    def action_show_view_menu(self) -> None:
        logs_visible = self.logWindow.display
        self.push_screen(ViewMenu(logs_visible), callback=self.on_view_menu_result)

    @on(events.Click, "#view_menu_label")
    def handle_view_click(self) -> None:
        logs_visible = self.logWindow.display
        self.push_screen(ViewMenu(logs_visible), callback=self.on_view_menu_result)

    def on_view_menu_result(self, result: str) -> None:
        """Handle the result from ViewMenu."""
        if result == "Show logs":
            self.logWindow.display = True
        elif result == "Hide logs":
            self.logWindow.display = False
        elif result == "Refresh":
            self.project.update_all()

    def __init__(self):
        super().__init__()

        pathname = str(Path.home() / ".gitter")

        # MainFileManager.shared = MainFile("untitled")
        # MainFileManager.shared.setupSampleData()
        # MainFileManager.save_shared_to_json(pathname)

        MainFileManager.load_shared_from_json(pathname)

        for project in MainFileManager.shared.projects:
            project.update()


if __name__ == "__main__":
    app = MenuApp()
    app.run()

