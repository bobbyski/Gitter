from pathlib import Path

from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Label, Markdown
from FileMenu import FileMenu
from MenuBar import MenuBar
from ProjectView import ProjectView
from ReleaseNotes import ReleaseNotesView
from ViewMenu import ViewMenu
from model.MainFileManager import MainFileManager
from model.Release import Release
from rich_log import RichLogWindow


class MenuApp(App):
    """A Textual app with a top menu bar and a 'File' popup menu."""
    
    CSS_PATH = ["menu_app.tcss", "project_view.tcss", "ReleaseNotes.tcss"]

    BINDINGS = [
        ("^q", "quit", "Quit"),
        # ("^f", "show_file_menu", "File Menu"),
    ]

    def app_container_class(self):
        return f"project_view {self.heightClass}"

    def compose(self) -> ComposeResult:

        self.project = ProjectView()
        self.logWindow = RichLogWindow()
        # self.update_markdown()
        self.releaseNotesWindow = ReleaseNotesView( self.releaseNotesText )
        self.appWindow = Horizontal(self.project, self.releaseNotesWindow, classes=f"app_window {self.app_container_class()}")

        yield Header()
        yield MenuBar()
        self.mainContainer = Container( self.appWindow, self.logWindow, classes="main_container", id="main_container")
        yield self.mainContainer
        yield Footer()

    def action_show_file_menu(self) -> None:
        self.push_screen(FileMenu())

    @on(events.Click, "#file_menu_label")
    def handle_file_click(self) -> None:
        self.push_screen(FileMenu())

    def action_show_view_menu(self) -> None:
        logs_visible = self.logWindow.display
        releasese_visible = self.releaseNotesWindow.display
        self.push_screen(ViewMenu(logs_visible, releasese_visible), callback=self.on_view_menu_result)

    @on(events.Click, "#view_menu_label")
    def handle_view_click(self) -> None:
        logs_visible = self.heightClass == "project_view_split_height"
        releasese_visible = self.releaseNotesWindow.display
        self.push_screen(ViewMenu(logs_visible, releasese_visible ), callback=self.on_view_menu_result)

    def on_view_menu_result(self, result: str) -> None:
        if result == "Show logs":
            self.logWindow.display = True
            self.project.post_message(ProjectView.ResizeRequested(height="project_view_split_height"))
            self.updateHeightClass()
        elif result == "Hide logs":
            self.logWindow.display = False
            self.project.post_message(ProjectView.ResizeRequested(height="project_view_full_height"))
            self.updateHeightClass()
        elif result == "Show release notes":
            self.releaseNotesWindow.display = True
            self.project.post_message(ProjectView.ResizeRequested(width="project_view_split_width"))
            self.updateWidthClass()
        elif result == "Hide release notes":
            self.releaseNotesWindow.display = False
            self.project.post_message(ProjectView.ResizeRequested(width="project_view_full_width"))
            self.updateWidthClass()
        elif result == "Refresh":
            self.post_message(ProjectView.RefreshRequested())
        self.refresh()

    def updateHeightClass(self):
        if self.heightClass == "project_view_full_height":
            self.heightClass = "project_view_split_height"
        else:
            self.heightClass = "project_view_full_height"
        self.refresh( recompose=True )

    def updateWidthClass(self):
        if self.widthClass == "project_view_full_width":
            self.widthClass = "project_view_split_width"
        else:
            self.widthClass = "project_view_full_width"
        self.project.post_message(ProjectView.ResizeRequested(width=self.widthClass))

    @on(ProjectView.ProjectSelected)
    def on_project_selected(self, message: ProjectView.ProjectSelected) -> None:
        self.project.selected_project = message.project
        self.update_markdown()
        # self.refresh(recompose=True)

    def update_markdown(self) -> None:
        # if self.releaseNotesWindow.markdown_content != self.lastMarkdown:
        if self.project.selected_project is not None:
            self.releaseNotesText = self.generate_markdown( self.project.selected_project )
        else:
            self.releaseNotesText = self.generate_release_notes_markdown()

        self.releaseNotesWindow.markdown_content = self.releaseNotesText
        self.lastMarkdown = self.releaseNotesText
        self.releaseNotesWindow.query_one(Markdown).update(self.releaseNotesText)
        # self.refresh( recompose=True )

    def generate_markdown(self, project ) -> str:
        markdown_lines = [f"#  {project.name} Release Notes"]
        current = project.current_release()

        if current != "":
            markdown_lines.append(f" - version: {current}")

        markdown_lines.append("\n")

        if project.releases:
            for release in project.releases:
                if len( release.issues ) > 0:
                    markdown_lines.append(f"## {release.name}")

                    markdown_lines.append( "\n" )

                    if release.issues:
                        for issue in release.issues:
                            if issue.number:
                                markdown_lines.append(f"#### {issue.number} \n")
                            markdown_lines.append(f"{issue.title}\n")

                    markdown_lines.append("\n")

        if len(markdown_lines) == 1:
            markdown_lines.append("No releases found.\n")

        return "".join(markdown_lines)


    def generate_release_notes_markdown(self) -> str:
        markdown_lines = ["# Release Notes\n"]

        if self.project.projects is None:
            return ""

        for project in self.project.projects:
            if project.releases:
                if len( project.issues_list() ) > 0:
                    markdown_lines.append(f"## {project.name}\n\n")
                    for release in project.releases:

                        if release.issues:
                            markdown_lines.append(f"### {release.name}\n")
                            for issue in release.issues:
                                if issue.number:
                                    markdown_lines.append(f"**{issue.number}**\n")
                                markdown_lines.append(f"{issue.title}\n")
                        markdown_lines.append("\n")

        return "".join(markdown_lines)

    def __init__(self):
        super().__init__()
        self.heightClass = "project_view_full_height"
        self.widthClass = "project_view_full_width"
        self.lastMarkdown = "qwerty"

        pathname = str(Path.home() / ".gitter")

        self.releaseNotesText = """
        # Release Notes
        
        Release notes text
        """

        self.project = ProjectView()
        self.logWindow = RichLogWindow()

        # MainFileManager.shared = MainFile("untitled")
        # MainFileManager.shared.setupSampleData()
        # MainFileManager.save_shared_to_json(pathname)

        MainFileManager.load_shared_from_json(pathname)

        for project in MainFileManager.shared.projects:
            project.update()


if __name__ == "__main__":
    app = MenuApp()
    app.run()

