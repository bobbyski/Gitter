from textual.app import ComposeResult
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Markdown, Static
from textual.containers import VerticalScroll


class ReleaseNotesView(Static):

    class ResizeRequested(Message):
        def __init__(self, width: str=None, height: str=None):
            self.width = width
            self.height = height
            super().__init__()

    CSS_PATH = ["TUI/project/ReleaseNotes.tcss", "TUI/project/project_view.tcss"]

    def __init__(self, markdown_content: str, title: str = "Release Notes"):
        super().__init__()
        self.markdown_content = markdown_content
        self.title_text = title

    def on_mount(self) -> None:
        self.border_title = self.title_text

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Markdown(self.markdown_content)

    def on_click(self) -> None:
        """Close the view when clicked outside."""
        self.dismiss()
