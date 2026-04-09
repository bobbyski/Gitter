from __future__ import annotations

from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical

from model.Project import Project


class FinishFeatureModal(ModalScreen[bool]):
    """Modal confirming finish of the current git-flow feature branch.

    Dismisses with True on Finish, or False on Cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        branch = project.status.branch if project.status else ""
        self._feature_name = branch.split("/", 1)[1] if "/" in branch else branch

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Finish Feature", id="finish_feature_title"),
            Label(
                f"Do you want to finish the feature: [bold cyan]{self._feature_name}[/bold cyan]?",
                id="finish_feature_message",
            ),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Finish", variant="primary", id="btn_finish"),
                id="finish_feature_buttons",
            ),
            id="finish_feature_container",
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
    def feature_name(self) -> str:
        return self._feature_name
