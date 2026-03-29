from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Markdown
from textual.containers import VerticalScroll


class ReleaseNotesView(ModalScreen):
    """A modal screen that displays release notes as rendered markdown."""

    CSS_PATH = "ReleaseNotes.tcss"

    def __init__(self, markdown_content: str, title: str = "Release Notes"):
        super().__init__()
        self.markdown_content = markdown_content
        self.title_text = title

    def compose(self) -> ComposeResult:
        with VerticalScroll() as scroll:
            scroll.border_title = self.title_text
            yield Markdown(self.markdown_content)

    def on_click(self) -> None:
        """Close the view when clicked outside."""
        self.dismiss()
