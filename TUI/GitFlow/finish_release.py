from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical

from model.Project import Project


class FinishReleaseModal(ModalScreen[bool]):
    """Modal confirming finish of the current git-flow release branch.

    Dismisses with True on Finish, or False on Cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        branch = project.status.branch if project.status else ""
        self._version = branch.split("/", 1)[1] if "/" in branch else branch

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Finish Release", id="finish_release_title"),
            Label(
                f"Do you want to finish release: [bold cyan]{self._version}[/bold cyan]?",
                id="finish_release_message",
            ),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Finish", variant="primary", id="btn_finish"),
                id="finish_release_buttons",
            ),
            id="finish_release_container",
        )

    def on_mount(self) -> None:
        self.query_one("#btn_finish", Button).focus()

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#btn_finish")
    def handle_finish(self) -> None:
        self.dismiss(True)

    @property
    def version(self) -> str:
        return self._version
