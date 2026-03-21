from textual.app import App, ComposeResult
from textual.widgets import Static, Label, DataTable
from textual.containers import VerticalScroll, Horizontal

from model.MainFileManager import MainFileManager
from model.Project import Project


class ProjectView(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = MainFileManager.shared.name
        self.projects = MainFileManager.shared.projects

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Label("Project Name", classes="header name"),
            Label("Directory", classes="header directory"),
            classes="row header-row"
        )
        with VerticalScroll(id="project_list"):
            for project in self.projects:
                row = Horizontal(
                    Label(project.name, classes="name"),
                    Label(project.directory, classes="directory"),
                    classes="row"
                )
                row.can_focus = True
                yield row


    def on_mount(self) -> None:
        self.border_title = self.title

class ProjectApp(App):
    CSS_PATH = "project_view.tcss"
    
    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
