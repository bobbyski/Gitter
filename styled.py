# from https://www.youtube.com/watch?v=dpJrM2_NOT8
# full course: https://realpython.com/videos/building-uis-terminal-textual-overview/

from textual.app import App
from textual.widgets import Label, Static


class StyledApp(App):
    CSS_PATH = "styled.tcss"

    def compose(self):
        yield Static("A static widget")
        yield Static("Using an id", id="static_with_id" )
        yield Static("First class", classes="static_cls1")
        yield Static("Second class", classes="static_cls1 static_cls2" )

    def on_key(self, event):
        match event.key:
            case "q":
                self.exit()
            case _:
                pass

if __name__ == "__main__":
    app = StyledApp()
    app.run()
