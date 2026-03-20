from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Label

class MenuBar(Static):
    """A simple menu bar at the top."""
    
    DEFAULT_CSS = """
    MenuBar {
        dock: top;
        height: 1;
        background: $accent;
        color: $text;
    }
    MenuBar > Horizontal {
        width: 100%;
    }
    MenuBar Label {
        padding: 0 2;
    }
    MenuBar Label:hover {
        background: $accent-darken-2;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("File", id="file_menu_label")
            yield Label("Edit")
            yield Label("View")
            yield Label("Help")
