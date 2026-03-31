from textual import on, events
from textual.app import App, ComposeResult
from textual.message import Message
from textual.widgets import Static, Label, Button, RichLog
from textual.containers import VerticalScroll, Horizontal, Vertical

from BusinessLogic.GitManager import GitManager
from model.MainFileManager import MainFileManager
from model.Project import Project
from ReleaseNotes import ReleaseNotesView
from rich_log import GitterLogger


class ProjectView(Static):
    class RefreshRequested(Message):
        """Message to request all ProjectView instances to refresh."""
        pass

    class ResizeRequested(Message):
        def __init__(self, width: str=None, height: str=None):
            self.width = width
            self.height = height
            super().__init__()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = MainFileManager.shared.name
        self.projects = MainFileManager.shared.projects
        self.widthClass = "project_view_split_width"
        self.classes = self.main_container_class()

    def main_container_class(self):
        return f"project_view {self.widthClass}"

    def compose(self) -> ComposeResult:
        self.classes = self.main_container_class()

        with Vertical():
            with Horizontal(classes="top-bar"):
                yield Button("Refresh", id="refresh_button", classes="toolbar_button")
                yield Button("Release notes", id="release_notes_button", classes="toolbar_button")
                yield Button("Add", id="add_button", classes="toolbar_button right_side")
                # yield Button("Logs", id="logs_button", classes="toolbar_button right_side")

            yield Horizontal(
                Label("Project Name", classes="header name"),
                Label("Directory", classes="header directory"),
                Label("Status", classes="header status"),
                Label("Next/Last Release", classes="header issues_list"),
                classes="row header-row"
            )

            with VerticalScroll(id="project_list"):
                for project in self.projects:
                    row = Horizontal(
                        Label(project.name, classes="name"),
                        Label(project.directory, classes="directory"),
                        Label(f"{project.status}", classes="status"),
                        Label(f"{project.issues_string_for_release()}", classes="issues_list"),
                        classes="row"
                    )
                    row.can_focus = True
                    yield row

    def on_mount(self) -> None:
        self.border_title = self.title
        self.set_interval(90, self.update_all)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        GitterLogger.log(f"Button pressed: {event.button.id}")
        if event.button.id == "refresh_button":
            self.update_all()
            self.refresh_table()
        elif event.button.id == "release_notes_button":
            # Generate release notes markdown
            markdown_content = self.generate_release_notes_markdown()
            GitterLogger.log(f"Markdown content:\n{markdown_content}")
        # elif event.button.id == "logs_button":
        #     if self.heightClass == "project_view_full_height":
        #         self.heightClass = "project_view_split_height"
        #     else:
        #         self.heightClass = "project_view_full_height"
        #     self.refresh(recompose=True)
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
            project.update()

            # GitterLogger.log( f"*****************************\nProject {project.name}\n*****************************" )
            # GitterLogger.log( project.releases )

        self.refresh( recompose=True )

    @on(RefreshRequested)
    def handle_refresh_requested(self, message: RefreshRequested) -> None:
        """Handle refresh request message."""
        self.update_all()

    @on(ResizeRequested)
    def handle_view_click(self, message: ResizeRequested) -> None:
        GitterLogger.log(f"ResizeRequested received - width: {message.width}, height: {message.height}")
        if message.width:
            self.widthClass = message.width

        if message.height:
            self.heightClass = message.height

        self.refresh( recompose=True )
        GitterLogger.log( "View menu clicked (ProjectView)" )

    def generate_release_notes_markdown(self) -> str:
        """Generate markdown content from all project releases."""
        markdown_lines = ["# Release Notes\n"]

        for project in self.projects:
            if project.releases:
                markdown_lines.append(f"## {project.name}\n")
                for release in project.releases:
                    markdown_lines.append(f"### {release.name}\n")
                    if release.issues:
                        for issue in release.issues:
                            markdown_lines.append(f"- {issue.title}\n")
                    else:
                        markdown_lines.append("- No issues listed\n")
                    markdown_lines.append("\n")

        if len(markdown_lines) == 1:
            markdown_lines.append("No releases found.\n")

        return "".join(markdown_lines)

class ProjectApp(App):
    CSS_PATH = "project_view.tcss"

    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
