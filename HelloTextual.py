# from https://www.youtube.com/watch?v=dpJrM2_NOT8
from kivy.logger import Logger
from textual.app import App
from textual.widgets import Label, Static

class HelloTextual(App):
    def compose(self):
        self.static = Static("[bold red]Hello, [bold white]Textual [bold blue]World![/]")
        yield self.static
        self.label = Label("Well we did [yellow italic]something[/]!")
        yield self.label

    def on_mount(self):
        #style the static widget
        self.static.styles.background = "gray"
        self.static.border = ("solid", "red")
        self.static.styles.text_align = "center"
        self.static.styles.padding = 1, 1
        self.static.styles.margin = 4,4

        #style the static widget
        self.label.styles.background = "darkgreen"
        self.label.border = ("double", "red")
        self.label.styles.padding = 1, 1
        self.label.styles.margin = 2,4

        Logger.info("Hello, Textual World!")

    def on_key(self, event):
        match event.key:
            case "q":
                Logger.info("Quitting")


                self.exit()
            case _:
                pass

if __name__ == "__main__":
    app = HelloTextual()
    app.run()

