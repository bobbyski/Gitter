from __future__ import annotations

from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, TextArea
from textual.containers import Horizontal, Vertical

from model.Project import Project


class GitCommitModal(ModalScreen[Optional[str]]):
    """Modal for composing and submitting a git commit message.

    Dismisses with the commit message string on commit, or None on cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Commit — {self._project.name}", id="commit_title"),
            TextArea(id="commit_message"),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Commit", variant="primary", id="btn_commit"),
                id="commit_button_row",
            ),
            id="commit_container",
        )

    def on_mount(self) -> None:
        self.query_one("#commit_message", TextArea).focus()

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_commit")
    def handle_commit(self) -> None:
        message = self.query_one("#commit_message", TextArea).text.strip()
        if message:
            self.dismiss(message)
