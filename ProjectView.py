from textual.app import App, ComposeResult
from textual.widgets import Static, Label
from model.Project import Project


class ProjectView(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Project View"
        self.projects = []
        
        self.setupSampleData()

    def compose(self) -> ComposeResult:
        yield Label("Project View")


    def on_mount(self) -> None:
        self.border_title = self.title

    def setupSampleData(self):
        self.title = "Bobby's Project"
        self.projects = [
            Project(f"Project {i}", f"/path/to/project_{i.lower()}")
            for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ]
        # Adding a few more to reach 30
        self.projects.extend([
            Project("Project AA", "/path/to/project_aa"),
            Project("Project BB", "/path/to/project_bb"),
            Project("Project CC", "/path/to/project_cc"),
            Project("Project DD", "/path/to/project_dd")
        ])
        

class ProjectApp(App):
    CSS_PATH = "project_view.tcss"
    
    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
