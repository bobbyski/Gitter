from __future__ import annotations

from textual import on, events
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import OptionList

HELP_TOPICS = [
    ("Add",     "add.md"),
    ("Status",  "status.md"),
    ("Issues",  "issues.md"),
    ("Notes",   "notes.md"),
    ("Raw",     "raw.md"),
    ("TUI",     "tui.md"),
    ("Version", "version.md"),
    ("Help",    "help.md"),
]

ABOUT_LABEL = "About Gitter"
LICENSE_LABEL = "License"
LICENSE_FILE = "license.md"


class HelpMenu(ModalScreen[str]):
    """Modal menu listing help topics; dismisses with the selected filename."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        yield OptionList(
            ABOUT_LABEL,
            "---",
            *[label for label, _ in HELP_TOPICS],
            "---",
            LICENSE_LABEL,
            id="help_menu_list",
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(str(event.option.prompt))

    def on_click(self, event: events.Click) -> None:
        if event.widget is self:
            self.dismiss(None)
