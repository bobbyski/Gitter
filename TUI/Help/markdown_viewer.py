from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Markdown
from textual.containers import Vertical, VerticalScroll


class MarkdownViewerModal(ModalScreen):
    """Modal screen that displays a Markdown document."""

    BINDINGS = [("escape", "dismiss", "Close")]

    def __init__(self, content: str, title: str = ""):
        super().__init__()
        self._content = content
        self._title = title

    def compose(self) -> ComposeResult:
        with Vertical(id="markdown_viewer_container"):
            with VerticalScroll(id="markdown_viewer_scroll"):
                yield Markdown(self._content, id="markdown_viewer_content")
            yield Button("Close", variant="primary", id="btn_close")

    def on_mount(self) -> None:
        container = self.query_one("#markdown_viewer_container")
        if self._title:
            container.border_title = self._title
        self.query_one("#btn_close", Button).focus()

    @on(Button.Pressed, "#btn_close")
    def handle_close(self) -> None:
        self.dismiss()
