#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Markdown

from TUI.Menu.FileMenu import FileMenu
from TUI.Menu.GitMenu import GitMenu
from TUI.Menu.MenuBar import MenuBar
from TUI.project.add_or_edit_project import AddOrEditProject
from TUI.commit.git_commit import GitCommitModal
from TUI.GitFlow.start_feature import StartFeatureModal
from TUI.GitFlow.finish_feature import FinishFeatureModal
from TUI.GitFlow.start_release import StartReleaseModal
from TUI.GitFlow.finish_release import FinishReleaseModal
from TUI.Help.help_menu import HelpMenu, HELP_TOPICS, ABOUT_LABEL, LICENSE_LABEL, LICENSE_FILE
from TUI.Help.markdown_viewer import MarkdownViewerModal
from TUI.Help.about_gitter import AboutGitter
from TUI.project.ProjectView import ProjectView
from TUI.project.ReleaseNotes import ReleaseNotesView
from TUI.Menu.ViewMenu import ViewMenu
from model.MainFileManager import MainFileManager
from model.Project import Project
from TUI.debug.rich_log import GitterLogger, RichLogWindow


class MenuApp(App):
    """A Textual app with a top menu bar and a 'File' popup menu."""
    
    CSS_PATH = ["menu_app.tcss",
                "project/project_view.tcss",
                "project/ReleaseNotes.tcss",
                "project/add_or_edit_project.tcss",
                "commit/git_commit.tcss",
                "commit/git_staging.tcss",
                "GitFlow/start_feature.tcss",
                "GitFlow/finish_feature.tcss",
                "GitFlow/start_release.tcss",
                "GitFlow/finish_release.tcss",
                "Help/markdown_viewer.tcss",
                "Help/about_gitter.tcss"]

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+a", "add_project", "Add Project"),
        ("ctrl+e", "edit_project", "Edit Project"),
        ("ctrl+d", "delete_project", "Delete Project"),
        ("ctrl+k", "commit", "Commit"),
        ("ctrl+l", "show_log", "Show Log"),
        ("ctrl+r", "show_release_notes", "Show Release Notes"),
        ("ctrl+f", "show_file_menu", "File Menu"),
        ("ctrl+v", "show_view_menu", "View Menu"),
        ("ctrl+g", "show_git_menu", "Git Menu"),
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
        self.push_screen(FileMenu(), callback=self.on_file_menu_result)

    def action_add_project(self) -> None:
        self.push_screen(AddOrEditProject(None), callback=self.on_project_added)

    def action_edit_project(self) -> None:
        if self.project.selected_project is None:
            return
        self.push_screen(AddOrEditProject(self.project.selected_project), callback=self.project.on_project_edited)

    def action_commit(self) -> None:
        if self.project.selected_project is None:
            return
        self.push_screen(GitCommitModal(self.project.selected_project), callback=self.on_commit_result)

    def on_commit_result(self, result: Optional[tuple]) -> None:
        if result is None:
            return
        message, add_unstaged = result
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        success, output = GitManager(project.directory).commit(message, add_unstaged)
        GitterLogger.log(f"Commit {'succeeded' if success else 'failed'}: {output}")
        if success:
            project.update()
            self.project.refresh(recompose=True)
            self.update_markdown()

    def action_delete_project(self) -> None:
        if self.project.selected_project is None:
            return
        MainFileManager.shared.remove_project(self.project.selected_project)
        self.project.projects = MainFileManager.shared.projects
        self.project.selected_project = None
        self.project.refresh(recompose=True)
        MainFileManager.save_shared_to_json(str(Path.home() / ".gitter"))

    @on(events.Click, "#file_menu_label")
    def handle_file_click(self) -> None:
        self.push_screen(FileMenu(), callback=self.on_file_menu_result)

    def on_file_menu_result(self, result: str) -> None:
        if result == "New":
            self.add_project()

    def add_project(self) -> None:
        self.push_screen(AddOrEditProject(None), callback=self.on_project_added)

    def on_project_added(self, project: Project ) -> None:
        if project is None:
            return
        MainFileManager.shared.add_project(project)
        self.project.projects = MainFileManager.shared.projects
        self.project.refresh(recompose=True)

        MainFileManager.save_shared_to_json(str(Path.home() / ".gitter"))

    def action_show_log(self) -> None:
        if self.logWindow.display:
            self.on_view_menu_result("Hide logs")
        else:
            self.on_view_menu_result("Show logs")

    def action_show_release_notes(self) -> None:
        if self.releaseNotesWindow.display:
            self.on_view_menu_result("Hide release notes")
        else:
            self.on_view_menu_result("Show release notes")

    def action_show_view_menu(self) -> None:
        logs_visible = self.logWindow.display
        releasese_visible = self.releaseNotesWindow.display
        self.push_screen(ViewMenu(logs_visible, releasese_visible), callback=self.on_view_menu_result)

    @on(events.Click, "#view_menu_label")
    def handle_view_click(self) -> None:
        logs_visible = self.heightClass == "project_view_split_height"
        releasese_visible = self.releaseNotesWindow.display
        self.push_screen(ViewMenu(logs_visible, releasese_visible ), callback=self.on_view_menu_result)

    def _current_branch(self) -> str:
        p = self.project.selected_project
        if p and p.status and hasattr(p.status, "branch"):
            return p.status.branch
        return ""

    def action_show_git_menu(self) -> None:
        self.push_screen(GitMenu(self._current_branch(), project_selected=self.project.selected_project is not None), callback=self.on_git_menu_result)

    @on(events.Click, "#git_menu_label")
    def handle_git_click(self) -> None:
        self.push_screen(GitMenu(self._current_branch(), project_selected=self.project.selected_project is not None), callback=self.on_git_menu_result)

    def on_git_menu_result(self, result: Optional[str]) -> None:
        if result is None:
            return
        if self.project.selected_project is None:
            GitterLogger.log("No project selected for git operation.")
            return
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        manager = GitManager(project.directory)
        if result == "Commit":
            self.action_commit()
        elif result == "Pull":
            success, output = manager.pull()
            GitterLogger.log(f"Pull {'succeeded' if success else 'failed'}: {output}")
            if success:
                project.update()
                self.project.refresh(recompose=True)
                self.update_markdown()
        elif result == "Fetch":
            success, output = manager.fetch()
            GitterLogger.log(f"Fetch {'succeeded' if success else 'failed'}: {output}")
            if success:
                project.update()
                self.project.refresh(recompose=True)
                self.update_markdown()
        elif result == "Push":
            success, output = manager.push()
            GitterLogger.log(f"Push {'succeeded' if success else 'failed'}: {output}")
        elif result == "Push Main and Develop":
            success, output = manager.push_main_and_develop()
            GitterLogger.log(f"Push main and develop {'succeeded' if success else 'failed'}: {output}")
        elif result == "Start Feature":
            self.push_screen(StartFeatureModal(project), callback=self.on_start_feature_result)
        elif result == "Finish Feature":
            self.push_screen(FinishFeatureModal(project), callback=self.on_finish_feature_result)
        elif result == "Start Release":
            self.push_screen(StartReleaseModal(project), callback=self.on_start_release_result)
        elif result == "Finish Release":
            self.push_screen(FinishReleaseModal(project), callback=self.on_finish_release_result)

    def on_start_feature_result(self, name: Optional[str]) -> None:
        if not name:
            return
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        success, output = GitManager(project.directory).flow_feature_start(name)
        GitterLogger.log(f"Start feature '{name}' {'succeeded' if success else 'failed'}: {output}")
        if success:
            project.update()
            self.project.refresh(recompose=True)

    @on(events.Click, "#help_menu_label")
    def handle_help_click(self) -> None:
        self.push_screen(HelpMenu(), callback=self.on_help_menu_result)

    def on_help_menu_result(self, result: Optional[str]) -> None:
        if not result:
            return
        if result == ABOUT_LABEL:
            self.push_screen(AboutGitter())
            return
        if result == LICENSE_LABEL:
            filename = LICENSE_FILE
        else:
            filename = next((f for l, f in HELP_TOPICS if l == result), None)
        if not filename:
            return
        from BusinessLogic.docs_helper import get_document
        content = get_document(filename)
        if content is None:
            GitterLogger.log(f"Help file not found: {filename}")
            return
        self.push_screen(MarkdownViewerModal(content, title=result))

    def on_start_release_result(self, version: Optional[str]) -> None:
        if not version:
            return
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        success, output = GitManager(project.directory).flow_release_start(version)
        GitterLogger.log(f"Start release '{version}' {'succeeded' if success else 'failed'}: {output}")
        if success:
            project.update()
            self.project.refresh(recompose=True)

    def on_finish_release_result(self, confirmed: bool) -> None:
        if not confirmed:
            return
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        branch = project.status.branch if project.status else ""
        version = branch.split("/", 1)[1] if "/" in branch else branch
        success, output = GitManager(project.directory).flow_release_finish(version)
        GitterLogger.log(f"Finish release '{version}' {'succeeded' if success else 'failed'}: {output}")
        if success:
            project.update()
            self.project.refresh(recompose=True)
            self.update_markdown()

    def on_finish_feature_result(self, confirmed: bool) -> None:
        if not confirmed:
            return
        from BusinessLogic.GitManager import GitManager
        project = self.project.selected_project
        branch = project.status.branch if project.status else ""
        feature_name = branch.split("/", 1)[1] if "/" in branch else branch
        success, output = GitManager(project.directory).flow_feature_finish(feature_name)
        GitterLogger.log(f"Finish feature '{feature_name}' {'succeeded' if success else 'failed'}: {output}")
        if success:
            project.update()
            self.project.refresh(recompose=True)
            self.update_markdown()

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
            self.releaseNotesWindow.visible = True
            self.refresh( recompose=True)
        elif result == "Hide release notes":
            self.releaseNotesWindow.display = False
            self.project.post_message(ProjectView.ResizeRequested(width="project_view_full_width"))
            self.updateWidthClass()
            self.releaseNotesWindow.visible = False
            self.refresh( recompose=True)
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

        self.releaseNotesWindow.set_markdown( self.releaseNotesText )
        self.lastMarkdown = self.releaseNotesText
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

