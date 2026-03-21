from textual.app import App, ComposeResult
from textual.widgets import Static

class ProjectView(Static):
    """A widget that presents a black view with a double white border."""
    

class ProjectApp(App):
    """A simple Textual app to display ProjectView."""
    
    CSS_PATH = "project_view.tcss"
    
    def compose(self) -> ComposeResult:
        yield ProjectView()

if __name__ == "__main__":
    app = ProjectApp()
    app.run()
