from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Button, RichLog
from textual.containers import VerticalScroll, Horizontal, Vertical

from BusinessLogic.GitManager import GitManager
from model.MainFileManager import MainFileManager
from model.Project import Project
from rich_log import GitterLogger


class ProjectView(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = MainFileManager.shared.name
        self.projects = MainFileManager.shared.projects

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(classes="top-bar"):
                yield Button("Refresh", id="refresh_button", classes="toolbar_button")
                yield Button("Release notes", id="release_notes_button", classes="toolbar_button middle")
                yield Button("Add", id="add_button", classes="toolbar_button right_side")

            yield Horizontal(
                Label("Project Name", classes="header name"),
                Label("Directory", classes="header directory"),
                Label("Status", classes="header status"),
                classes="row header-row"
            )

            with VerticalScroll(id="project_list"):
                for project in self.projects:
                    row = Horizontal(
                        Label(project.name, classes="name"),
                        Label(project.directory, classes="directory"),
                        Label(f"{project.status}", classes="status"),
                        classes="row"
                    )
                    row.can_focus = True
                    yield row

    def on_mount(self) -> None:
        self.border_title = self.title

    def on_button_pressed(self, event: Button.Pressed) -> None:
        GitterLogger.log(f"Button pressed: {event.button.id}")
        if event.button.id == "refresh_button":
            self.update_all()
            self.refresh_table()
        elif event.button.id == "add_button":
            # Stub for future add behavior
            pass

    def refresh_table(self) -> None:
        project_list = self.query_one("#project_list", VerticalScroll)
        project_list.remove_children()

        for project in self.projects:
            row = Horizontal(
                Label(project.name, classes="name"),
                Label(project.directory, classes="directory"),
                Label(f"{project.status}", classes="status"),
                classes="row"
            )
            row.can_focus = True
            project_list.mount(row)

    def update_all(self):

        GitterLogger.log( "Updating all projects" )
        for project in self.projects:
            project.update_status()

            project.commits = GitManager(project.directory).get_logs()
            project.process_commits()

            GitterLogger.log( f"*****************************\nProject {project.name}\n*****************************" )
            GitterLogger.log( project.releases )


class ProjectApp(App):
    CSS_PATH = "project_view.tcss"

    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
