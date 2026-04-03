from __future__ import annotations

import csv
import io

from rich.console import RenderableType
from rich.syntax import Syntax
from rich.table import Table

from textual import events
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import RichLog, Static

CSV = """lane,swimmer,country,time
4,Joseph Schooling,Singapore,50.39
2,Michael Phelps,United States,51.14
5,Chad le Clos,South Africa,51.14
6,László Cseh,Hungary,51.14
3,Li Zhuhao,China,51.26
8,Mehdy Metella,France,51.58
7,Tom Shields,United States,51.73
1,Aleksandr Sadovnikov,Russia,51.84"""


CODE = '''\
def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value\
'''
class RichLogWindow(Static):
    queuedLogs = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Debug Log"
        GitterLogger.logView = self

    def compose(self) -> ComposeResult:
        GitterLogger.logView = self
        yield RichLog(highlight=True, markup=True)

    def on_mount(self) -> None:
        # note this code is not yet working - not a priority - will fix later
        if GitterLogger.logView is not None:
            try:
                text_log = self.query_one(RichLog)
                logs = GitterLogger.queuedLogs
                GitterLogger.queuedLogs.clear()
                for message in logs:
                    text_log.write(message)
            except Exception:
                pass

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        text_log = self.query_one(RichLog)

        text_log.write(Syntax(CODE, "python", indent_guides=True))

        rows = iter(csv.reader(io.StringIO(CSV)))
        table = Table(*next(rows))
        for row in rows:
            table.add_row(*row)

        text_log.write(table)
        text_log.write("[bold magenta]Write text or any Rich renderable!")

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        text_log = self.query_one(RichLog)
        text_log.write(event)


class GitterLogger:
    logView: RichLogWindow = None
    queuedLogs = []

    @classmethod
    def log(cls, message: RenderableType | object):
        if GitterLogger.logView is None:
            GitterLogger.queuedLogs.append(message)
        else:
            try:
                GitterLogger.logView.query_one(RichLog).write(message)
            except Exception:
                GitterLogger.queuedLogs.append(message)

class RichLogApp(App):
    def compose(self) -> ComposeResult:
        yield RichLogWindow()

if __name__ == "__main__":
    app = RichLogApp()
    app.run()
