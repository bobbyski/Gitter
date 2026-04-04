from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, DirectoryTree, Input, Label, Static
from textual.containers import Horizontal, Vertical, VerticalScroll

from model.Project import Project
from model.GitLog import GitLog


class VisibleDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [p for p in paths if not p.name.startswith(".")]


class DirectoryPickerModal(ModalScreen[Optional[str]]):
    """A modal that lets the user pick a directory using DirectoryTree."""

    def __init__(self, start_path: str = ""):
        super().__init__()
        self._start = Path(start_path).expanduser() if start_path else Path.home()
        if not self._start.is_dir():
            self._start = Path.home()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Select Directory", id="picker_title"),
            VisibleDirectoryTree(str(self._start), id="dir_tree"),
            Horizontal(
                Button("Cancel", variant="default", id="picker_cancel"),
                Button("Select", variant="primary", id="picker_select"),
                id="picker_button_row",
            ),
            id="picker_container",
        )

    @on(DirectoryTree.DirectorySelected)
    def handle_dir_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self._selected = str(event.path)

    @on(Button.Pressed, "#picker_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#picker_select")
    def handle_select(self) -> None:
        selected = getattr(self, "_selected", None)
        self.dismiss(selected)


class AddOrEditProject(ModalScreen[Optional[Project]]):
    """Modal for adding a new project or editing an existing one.

    Dismisses with the updated/new Project on save, or None on cancel.
    """

    def __init__(self, project: Project ):
        super().__init__()
        self._project = project
        self.border_title = "Add Project" if project is None else "Edit Project"

    def compose(self) -> ComposeResult:
        p = self._project
        yield Vertical(
            # Label("Edit Project" if p else "Add Project", id="modal_title"),
            VerticalScroll (
                Label("Name"),
                Input(value=p.name if p else "", placeholder="Project name", id="input_name"),
                Label("Directory"),
                Horizontal(
                    Input(value=p.directory if p else "", placeholder="/path/to/repo", id="input_directory"),
                    Button("Browse", variant="default", id="btn_browse"),
                    id="directory_row",
                ),
                Label("Tag Branch"),
                Input(value=p.tagBranch if p else "", placeholder="main", id="input_tag_branch"),
                Label("Issue Prefixes  (comma-separated)"),
                Input(
                    value=", ".join(p.issuePrefixes) if p else "",
                    placeholder="GIT, PROJ",
                    id="input_issue_prefixes",
                ),
                Label("PR Patterns  (comma-separated)"),
                Input(
                    value=", ".join(p.prPatterns) if p else "",
                    placeholder="#(\\d+)",
                    id="input_pr_patterns",
                ),
                Label("Groups  (comma-separated)"),
                Input(
                    value=", ".join(p.groups) if p else "",
                    placeholder="backend, infra",
                    id="input_groups",
                ),
                Checkbox("Favorite", value=p.favorite if p else False, id="input_favorite"),
                id="scroll_container"
            ),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Save", variant="primary", id="btn_save"),
                id="button_row",
            ),
            id="modal_container",
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _split(self, raw: str) -> list[str]:
        """Split a comma-separated string into a stripped, non-empty list."""
        return [s.strip() for s in raw.split(",") if s.strip()]

    def _build_project(self) -> Project:
        p = self._project
        return Project(
            name=self.query_one("#input_name", Input).value.strip(),
            directory=self.query_one("#input_directory", Input).value.strip(),
            tagBranch=self.query_one("#input_tag_branch", Input).value.strip(),
            issuePrefixes=self._split(self.query_one("#input_issue_prefixes", Input).value),
            prPatterns=self._split(self.query_one("#input_pr_patterns", Input).value),
            groups=self._split(self.query_one("#input_groups", Input).value),
            favorite=self.query_one("#input_favorite", Checkbox).value,
            # Preserve live data when editing; start empty for new projects.
            status=p.status if p else "",
            commits=p.commits if p else [],
            issues=p.issues if p else [],
            releases=p.releases if p else [],
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    @on(Button.Pressed, "#btn_browse")
    def handle_browse(self) -> None:
        current = self.query_one("#input_directory", Input).value.strip()
        def on_picked(path: str | None) -> None:
            if path:
                self.query_one("#input_directory", Input).value = path
        self.app.push_screen(DirectoryPickerModal(current), callback=on_picked)

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_save")
    def handle_save(self) -> None:
        self.dismiss(self._build_project())
