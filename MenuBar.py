from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Label

class MenuBar(Static):
    """A simple menu bar at the top."""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("File", id="file_menu_label")
            yield Label("Edit")
            yield Label("View")
            yield Label("Help")
