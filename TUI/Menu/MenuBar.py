from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Label

class MenuBar(Static):
    """A simple menu bar at the top."""
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("File", id="file_menu_label")
            yield Label("Edit")
            yield Label("View", id="view_menu_label")
            yield Label("Git", id="git_menu_label")
            yield Label("Help")
