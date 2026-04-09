from __future__ import annotations

from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Horizontal, Vertical

from model.Project import Project


class StartFeatureModal(ModalScreen[Optional[str]]):
    """Modal for starting a new git-flow feature branch.

    Dismisses with the feature name string on Start, or None on Cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Start Feature — {self._project.name}", id="start_feature_title"),
            Label("Feature name", classes="start_feature_label"),
            Input(placeholder="my-feature", id="feature_name"),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Start", variant="primary", id="btn_start"),
                id="start_feature_buttons",
            ),
            id="start_feature_container",
        )

    def on_mount(self) -> None:
        self.query_one("#feature_name", Input).focus()

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_start")
    def handle_start(self) -> None:
        name = self.query_one("#feature_name", Input).value.strip()
        if name:
            self.dismiss(name)
