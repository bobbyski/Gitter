from __future__ import annotations

from textual import on, events
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Vertical, Horizontal

from BusinessLogic.toml_helper import TomlHelper


class AboutGitter(ModalScreen):
    """Modal about box showing app info, version, and credits."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        version = TomlHelper().get_version()
        yield Vertical(
            Label("Gitter", id="about_title"),
            Label(f"Version {version}", id="about_version"),
            Label("", id="about_spacer"),
            Label("Monitor multiple Git repositories from your terminal.", id="about_description"),
            Label("", id="about_spacer2"),
            Label("Built with:", id="about_built_with_label"),
            Horizontal(
                Label("  \u2022 Textual", classes="about_credit"),
                Label("  \u2022 Rich", classes="about_credit"),
                id="about_credits",
            ),
            Label("", id="about_spacer3"),
            Label("\u00a9 2026 Bobby Skinner. All rights reserved.", id="about_copyright"),
            Label("", id="about_spacer4"),
            Button("Close", variant="primary", id="btn_close"),
            id="about_container",
        )

    def on_mount(self) -> None:
        self.query_one("#btn_close", Button).focus()

    @on(Button.Pressed, "#btn_close")
    def handle_close(self) -> None:
        self.dismiss()

    def on_click(self, event: events.Click) -> None:
        if event.widget is self:
            self.dismiss()
