from __future__ import annotations

from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Button, Label, Static
from textual.containers import Horizontal, Vertical, VerticalScroll

from model.GitStatus import GitStatus


class GitStagingView(Static):
    """A reusable view showing staged and unstaged files with stage/unstage controls."""

    class StageAll(Message):
        pass

    class UnstageAll(Message):
        pass

    def __init__(self, git_status: GitStatus, **kwargs):
        super().__init__(**kwargs)
        self._git_status = git_status

    def compose(self) -> ComposeResult:
        staged = self._git_status.stagedFiles if self._git_status else []
        unstaged = self._git_status.unstagedFiles if self._git_status else []

        with Vertical(id="staging_container"):
            with VerticalScroll(id="staged_box"):
                for f in staged:
                    yield Horizontal(
                        Label(f.state, classes="staging_state"),
                        Label(f.filename, classes="staging_filename"),
                        classes="staging_row",
                    )

            with Horizontal(id="staging_buttons"):
                yield Button("↑  Stage all", id="btn_stage_all", variant="primary")
                yield Button("↓  Unstage all", id="btn_unstage_all", variant="default")

            with VerticalScroll(id="unstaged_box"):
                for f in unstaged:
                    yield Horizontal(
                        Label(f.state, classes="staging_state"),
                        Label(f.filename, classes="staging_filename"),
                        classes="staging_row",
                    )

    def on_mount(self) -> None:
        self.query_one("#staged_box").border_title = "Staged"
        self.query_one("#unstaged_box").border_title = "Unstaged"

    @on(Button.Pressed, "#btn_stage_all")
    def handle_stage_all(self) -> None:
        self.post_message(self.StageAll())

    @on(Button.Pressed, "#btn_unstage_all")
    def handle_unstage_all(self) -> None:
        self.post_message(self.UnstageAll())
