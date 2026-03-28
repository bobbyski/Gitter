from textual import on
from textual.app import ComposeResult
from textual.widgets import OptionList
from textual.screen import ModalScreen

class ViewMenu(ModalScreen):
    logsString = "Show logs"

    def compose(self) -> ComposeResult:
        yield OptionList(
            "Refresh",
            "---",
            ViewMenu.logsString,
            id="view_list"
        )

    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        if str(event.option.prompt) == ViewMenu.logsString:
            if ViewMenu.logsString == "Show logs":
                ViewMenu.logsString = "Hide logs"
        elif str(event.option.prompt) == "Refresh":
            self.app.refresh()
        else:
                ViewMenu.logsString = "Show logs"

        # else:
            # For other options, just close the menu
            # self.dismiss()

    def on_click(self) -> None:
        # Close the menu if clicked outside
        self.dismiss()
