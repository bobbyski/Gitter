import asyncio
from typing import List
from textual import on, work
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Log
from textual.worker import Worker
from textual.app import ComposeResult

class LogScreen(ModalScreen):
    count = reactive(0)
    MAX_LINES = 10_000
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "log_screen.tcss"

    def __init__(
            self,
            name: str | None = None,
            ident: str | None = None,
            classes: str | None = None,
            selections: List = None
    ):
        super().__init__(name, ident, classes)
        self.selections = selections

    def compose(self) -> ComposeResult:
        yield Label(f"Running {len(self.selections)} commands")
        event_log = Log(
            id='event_log',
            max_lines=LogScreen.MAX_LINES,
            highlight=True
        )
        event_log.loading = True
        yield event_log
        button = Button("Close", id="close", variant="success")
        button.disabled = True
        yield button

    async def on_mount(self) -> None:
        event_log = self.query_one('#event_log', Log)
        event_log.loading = False
        event_log.clear()
        lst = '\n'.join(self.selections)
        event_log.write(f"Preparing:\n{lst}")
        event_log.write("\n")

        for command in self.selections:
            self.count += 1
            self.run_process(cmd=command)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if self.count == 0:
            button = self.query_one('#close', Button)
            button.disabled = False
        self.log(event)

    @work(exclusive=False)
    async def run_process(self, cmd: str) -> None:
        event_log = self.query_one('#event_log', Log)
        event_log.write_line(f"Running: {cmd}")
        # Combine STDOUT and STDERR output
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        stdout, _ = await proc.communicate()
        if proc.returncode != 0:
            raise ValueError(f"'{cmd}' finished with errors ({proc.returncode})")
        stdout = stdout.decode(encoding='utf-8', errors='replace')
        if stdout:
            event_log.write(f'\nOutput of "{cmd}":\n')
            event_log.write(stdout)
        self.count -= 1

    @on(Button.Pressed, "#close")
    def on_button_pressed(self, _) -> None:
        self.app.pop_screen()
