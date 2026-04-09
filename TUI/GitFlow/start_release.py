from __future__ import annotations

import re
from typing import Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.containers import Horizontal, Vertical

from model.Project import Project


def _increment_version(version: str) -> str:
    """Increment the trailing component of a version string.

    Examples:
        1.0.1    -> 1.0.2
        1.1.0RC2 -> 1.1.0RC3
        1.2.3a   -> 1.2.3b
    """
    if not version:
        return version

    # Trailing number (handles "1.0.1" and "1.1.0RC2")
    match = re.search(r"(\d+)$", version)
    if match:
        n = int(match.group(1))
        return version[: match.start()] + str(n + 1)

    # Trailing single lowercase letter (handles "1.2.3a")
    match = re.search(r"([a-z])$", version)
    if match:
        return version[: match.start()] + chr(ord(match.group(1)) + 1)

    # Trailing single uppercase letter
    match = re.search(r"([A-Z])$", version)
    if match:
        return version[: match.start()] + chr(ord(match.group(1)) + 1)

    return version


class StartReleaseModal(ModalScreen[Optional[str]]):
    """Modal for starting a new git-flow release branch.

    Dismisses with the version string on Start, or None on Cancel.
    """

    def __init__(self, project: Project):
        super().__init__()
        self._project = project
        current = project.current_release() or ""
        self._next_version = _increment_version(current)

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Start Release — {self._project.name}", id="start_release_title"),
            Label("Version", classes="start_release_label"),
            Input(value=self._next_version, placeholder="1.0.0", id="release_version"),
            Horizontal(
                Button("Cancel", variant="default", id="btn_cancel"),
                Button("Start", variant="primary", id="btn_start"),
                id="start_release_buttons",
            ),
            id="start_release_container",
        )

    def on_mount(self) -> None:
        self.query_one("#release_version", Input).focus()

    @on(Button.Pressed, "#btn_cancel")
    def handle_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_start")
    def handle_start(self) -> None:
        version = self.query_one("#release_version", Input).value.strip()
        if version:
            self.dismiss(version)
