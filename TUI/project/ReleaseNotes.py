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
        self.set_markdown(markdown_content, refresh=False )
        self.title_text = title

    def on_mount(self) -> None:
        self.border_title = self.title_text

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Markdown(self.markdown_content)

    def on_click(self) -> None:
        """Close the view when clicked outside."""
        self.dismiss()

    def set_markdown(self, markdown_content: str, refresh: bool = True, max_lines: int = 5000 ) -> None:
        """Update the markdown content displayed in the view."""
        lines = markdown_content.splitlines()
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines.append(f"\n*... truncated at {max_lines} lines (use gitter -p <project> notes to see all) ...*")
        self.markdown_content = "\n".join(lines)
        if refresh:
            self.query_one(Markdown).update(self.markdown_content)

