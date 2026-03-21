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
        
        # self.setupSampleData()

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

    # def setupSampleData(self):
    #     self.title = "Bobby's Project"
    #     self.projects = [
    #         Project(f"Project {i}", f"/path/to/project_{i.lower()}")
    #         for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    #     ]
    #     # Adding a few more to reach 30
    #     self.projects.extend([
    #         Project("Project Aardvark Adventures with the amazing Andrew Abernathy", "/path/to/project_aa"),
    #         Project("Project BB", "/path/to/project_bb"),
    #         Project("Project CC", "/path/to/project_cc"),
    #         Project("Project DD", "/path/to/project_dd"),
    #         Project("Project EE", "/path/to/project_ee"),
    #         Project("Project FF", "/path/to/project_ff"),
    #         Project("Project GG", "/path/to/project_gg"),
    #
    #         # add a long text place holde rto test limits
    #         Project("Project HH", """We the People of the United States, in order to form a more perfect union,
    #                               establish justice, insure domestic tranquility, provide for the common defense,
    #                               promote the general welfare, and secure the blessings of liberty to ourselves and
    #                               our posterity, do ordain and establish this Constitution for the United States of
    #                               America.
    #                               """)
    #     ])
        

class ProjectApp(App):
    CSS_PATH = "project_view.tcss"
    
    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
